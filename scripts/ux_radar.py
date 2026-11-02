#!/usr/bin/env python3
"""Design/UX radar for the Drupal AI Initiative. Zero config, stdlib only, anonymous API, read-only.

  python3 scripts/ux_radar.py            # markdown report (default)
  python3 scripts/ux_radar.py --lite     # three fetches only: requests, story reviews, UX meeting
  python3 scripts/ux_radar.py --tsv      # one row per candidate
  python3 scripts/ux_radar.py --json
  python3 scripts/ux_radar.py --sprint 21   # skip sprint detection

Env: DRUPALCODE_API overrides https://git.drupalcode.org/api/v4.
Label census for maintenance (run monthly, adjust REQUEST_LABELS / SCOPED_LABELS):
  curl -sI "$API/groups/project/issues?state=opened&labels=<label>&per_page=1" | grep -i x-total:
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = os.environ.get("DRUPALCODE_API", "https://git.drupalcode.org/api/v4").rstrip("/")
GROUP = "groups/project"
UA = "drupal-ai-ux-contrib/ux_radar (read-only)"
GL = "https://git.drupalcode.org/project/"

# Sprint 21 began 2026-11-02 on a two-week cadence; the probe starts one below the date estimate.
SPRINT_ANCHOR = (21, dt.date(2026, 11, 2))
SPRINT_FLOOR = 20

REQUEST_LABELS = ["Needs UX review", "needs ux review"]            # instance-wide by design
SCOPED_LABELS = ["what::ux", "ux", "ui", "accessibility", "Accessibility", "Needs design"]  # initiative projects only
TITLE_KEYWORDS = re.compile(
    r"\b(UX|UI|usability|accessib\w*|WCAG|design|labels?|wording|icons?|dialogs?|modal|story|stories|"
    r"help text|naming|rename|screen ?reader|keyboard|contrast|first[- ]impression|user experience)\b", re.I)
DEMO_KEYWORDS = re.compile(
    r"\b(UX|UI|button|menu|link|page|upload|message|dialog|consent|story|stories|label|icon|text|review|"
    r"experience|feature page|screenshot|wording|instructions?)\b", re.I)
TERMINAL = {"state::fixed", "state::closed", "state::postponed", "state::blocked", "state::inProgress", "state::rtbc"}
ASK_FIRST_PROJECTS = {"canvas"}   # own design team; ask in #ai-ux before picking
MEETING_TITLE = re.compile(r"Drupal AI UX meeting (\d{1,2} \w+ \d{4})", re.I)
LANES = ["story-review", "review-request", "accessibility", "content-naming", "design-exploration",
         "research-ia", "housekeeping", "other-ux"]
GUIDE = {"story-review": "guide/04-story-review.md", "review-request": "guide/05-answer-a-ux-review-request.md",
         "accessibility": "guide/06-file-a-ux-issue.md", "content-naming": "guide/06-file-a-ux-issue.md",
         "design-exploration": "guide/06-file-a-ux-issue.md", "research-ia": "guide/03-where-the-work-is.md",
         "housekeeping": "guide/03-where-the-work-is.md", "other-ux": "guide/06-file-a-ux-issue.md"}


# ---------- HTTP ----------
def get(path, params=None, want_headers=False):
    url = f"{API}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params, safe=":,[]")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = json.loads(r.read() or b"null")
            return (r.headers, body) if want_headers else body
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"warn: {e.code} {url}\n")
        return ({}, []) if want_headers else []
    except urllib.error.URLError as e:
        sys.exit(f"error: {e.reason} {url}")


def total(path, params):
    headers, _ = get(path, dict(params, per_page=1), want_headers=True)
    try:
        return int(headers.get("x-total", "0"))
    except ValueError:
        return 0


def pages(path, params, max_pages=4):
    out = []
    for page in range(1, max_pages + 1):
        chunk = get(path, dict(params, per_page=100, page=page))
        if not isinstance(chunk, list) or not chunk:
            break
        out.extend(chunk)
        if len(chunk) < 100:
            break
    return out


# ---------- sprint ----------
def detect_sprint(today, override=None):
    """Highest 2026SprintNN active on project ai; probes upward from a date estimate until two empty labels."""
    if override:
        return override, []
    n0, d0 = SPRINT_ANCHOR
    start = max(SPRINT_FLOOR, n0 + (today - d0).days // 14 - 1)
    rows, empty, n = [], 0, start
    while empty < 2 and n < start + 8:
        label = f"2026Sprint{n}"
        g = total(f"{GROUP}/issues", {"state": "opened", "labels": label})
        a = total("projects/project%2Fai/issues", {"state": "opened", "labels": label}) if g else 0
        rows.append((n, g, a))
        empty = empty + 1 if g == 0 else 0
        n += 1
    active_ai = [n for n, g, a in rows if a >= 1]
    active_group = [n for n, g, a in rows if g >= 1]
    return (max(active_ai) if active_ai else max(active_group) if active_group else start), rows


# ---------- classify ----------
def norm(issue, source):
    ref = issue["references"]["full"].replace("project/", "")
    return {"ref": ref, "project": ref.split("#")[0], "iid": issue["iid"], "title": issue["title"],
            "labels": issue.get("labels") or [], "assignees": [a["username"] for a in issue.get("assignees") or []],
            "updated": issue["updated_at"][:10], "url": GL + ref.replace("#", "/-/issues/"), "sources": {source}}


def lane_for(it):
    t, p = it["title"], it["project"]
    labels_l = {l.lower() for l in it["labels"]}
    if p == "ai_demo" and re.search(r"UX review:|story|first[- ]impression", t, re.I):
        return "story-review"
    if p == "ai_initiative" and ("documentation" in labels_l or re.search(r"documentation|docs|meeting notes", t, re.I)):
        return "housekeeping"
    if "needs ux review" in labels_l:
        return "review-request"
    if "accessibility" in labels_l or re.search(r"accessib|WCAG|screen ?reader|keyboard|contrast", t, re.I):
        return "accessibility"
    if "category::plan" in labels_l or re.search(r"\[(Meta|Plan)\]|\bMETA\b|roadmap|research|journey|information architecture|stream\b", t, re.I):
        return "research-ia"
    if re.search(r"\blabels?\b|wording|help text|naming|rename|terminolog|typo|\btext\b|\bicons?\b|\bdescriptions?\b|instructions?", t, re.I):
        return "content-naming"
    if "needs design" in labels_l or re.search(
            r"choose a fix|UI changes|\bUI\b|design|sketch|mockup|wireframe|layout|dialog|modal|redesign|explorer|"
            r"improve .*UX|\bUX\b|filter|listing|sorting|remember|reset button|show more|button|menu|navigation|scroll", t, re.I):
        return "design-exploration"
    return "other-ux"


def signals(it, current_label, today):
    s = []
    s.append("claimed:" + ",".join(it["assignees"]) if it["assignees"] else "unclaimed")
    if it["project"] == "ai_demo":
        s.append("forge")  # reproducible on a Drupal Forge demo instance
    if current_label in it["labels"]:
        s.append("sprint")
    if any(l.lower() == "needs ux review" for l in it["labels"]):
        s.append(f"age:{(today - dt.date.fromisoformat(it['updated'])).days}d")
    if any(l.lower().startswith("novice") for l in it["labels"]):
        s.append("novice")
    if it["project"] in ASK_FIRST_PROJECTS:
        s.append("ask-first")
    term = sorted(l for l in it["labels"] if l in TERMINAL)
    if term:
        s.append("terminal:" + ",".join(term))
    return s


def meetings(today):
    rows = get("projects/project%2Fai_initiative/issues",
               {"search": "UX meeting", "in": "title", "per_page": 100, "order_by": "created_at"})
    dated = []
    for r in rows or []:
        m = MEETING_TITLE.search(r["title"])
        if m:
            try:
                dated.append((dt.datetime.strptime(m.group(1), "%d %B %Y").date(), r))
            except ValueError:
                pass
    dated.sort(key=lambda x: x[0])
    out = {}
    up = [x for x in dated if x[0] >= today]
    past = [x for x in dated if x[0] < today]
    if up:
        out["next"] = up[0]
    if past:
        out["previous"] = past[-1]
    return out


# ---------- collect ----------
def collect(current_label, lite):
    items = {}

    def add(issues, source, keep=lambda i: True):
        for i in issues or []:
            if not keep(i):
                continue
            n = norm(i, source)
            items.setdefault(n["ref"], n)["sources"].add(source)

    for label in REQUEST_LABELS:
        add(pages(f"{GROUP}/issues", {"state": "opened", "labels": label}, max_pages=1), f"label:{label}")
    demo = pages("projects/project%2Fai_demo/issues", {"state": "opened"}, max_pages=1)
    add(demo, "ai_demo", lambda i: bool(DEMO_KEYWORDS.search(i["title"]))
        or bool({l.lower() for l in i.get("labels") or []} & {"ui", "ux", "needs ux review"}))
    if lite:
        return items, set()

    sprint_issues = pages(f"{GROUP}/issues", {"state": "opened", "labels": current_label})
    init_issues = pages(f"{GROUP}/issues", {"state": "opened", "labels": "AI Initiative Sprint"}, max_pages=3)
    projects = {i["references"]["full"].split("#")[0].replace("project/", "") for i in sprint_issues + init_issues}
    projects |= {"ai_demo", "ai_initiative", "ai", "ai_context", "ai_agents", "ai_ckeditor", "canvas"}
    add(sprint_issues, "sprint-keyword", lambda i: bool(TITLE_KEYWORDS.search(i["title"])))
    add(init_issues, "initiative-keyword", lambda i: bool(TITLE_KEYWORDS.search(i["title"])))
    for label in SCOPED_LABELS:
        add(pages(f"{GROUP}/issues", {"state": "opened", "labels": label}, max_pages=1), f"label:{label}",
            lambda i: i["references"]["full"].split("#")[0].replace("project/", "") in projects)
    return items, projects


# ---------- output ----------
def link(it):
    return f"[{it['ref']}]({it['url']})"


def row(it):
    sig = ", ".join(s for s in it["signals"] if not s.startswith("terminal:"))
    return f"- {link(it)} — {it['title']} ({sig}; updated {it['updated']})"


def section(title, rows, empty="none found", cap=None):
    out = [f"## {title}", ""]
    shown = rows[:cap] if cap else rows
    out += [row(r) for r in shown] if rows else [empty]
    if cap and len(rows) > cap:
        out.append(f"- … {len(rows) - cap} more; `--tsv` lists everything.")
    out.append("")
    return out


def excerpt(desc, limit=2500):
    desc = (desc or "").strip()
    if not desc:
        return "(no notes yet)"
    # Prefer the parts a designer needs: decisions, next steps, next story reviews.
    keep = []
    for h in ("Next story reviews", "Decisions", "Questions", "Next Steps"):
        m = re.search(rf"#+\s*{h}.*?(?=\n#|\Z)", desc, re.S | re.I)
        if m:
            keep.append(m.group(0).strip())
    text = "\n\n".join(keep) if keep else desc
    text = re.sub(r"(?m)^#{1,6}\s*", "#### ", text)  # keep the report's own section levels
    return text[:limit] + (f"\n… ({len(text) - limit} more chars; open the issue)" if len(text) > limit else "")


def report(rows, current, probe, mtg, today, lite):
    label = f"2026Sprint{current}"
    live = [r for r in rows if not any(s.startswith("terminal:") for s in r["signals"])]
    claimed = lambda r: any(s.startswith("claimed:") for s in r["signals"])
    ask = lambda r: "ask-first" in r["signals"]
    open_ = [r for r in live if not claimed(r) and not ask(r)]
    watch = [r for r in live if claimed(r) and not ask(r)]
    canvas = [r for r in live if ask(r)]
    by = lambda lane, pool: [r for r in pool if r["lane"] == lane]
    out = [f"# AI UX radar — {today}", "",
           f"{'Lite scan (requests, story reviews, meeting). ' if lite else ''}Sprint {label}"
           + (f" (open issues group/ai: " + ", ".join(f"S{n} {g}/{a}" for n, g, a in probe) + ")" if probe else "")
           + f". {len(live)} open candidates, {len(open_)} unclaimed. Point-in-time; recheck before claiming.", ""]
    out += ["## This Monday's UX meeting", ""]
    for key, lab in (("next", "Next"), ("previous", "Previous")):
        if key in mtg:
            d, r = mtg[key]
            out += [f"**{lab}: {d}** — [{r['title']}]({GL}ai_initiative/-/issues/{r['iid']})", "",
                    excerpt(r.get("description")) if key == "previous" or (r.get("description") or "").strip() else "(agenda not posted yet)", ""]
    if not mtg:
        out += ["none found", ""]
    out += section("Story reviews (unclaimed first)", by("story-review", open_) + by("story-review", watch))
    reqs = sorted(by("review-request", open_), key=lambda r: r["updated"])
    out += section("UX review requests (oldest first; SLA is 3 business days)", reqs)
    if not lite:
        mid = by("accessibility", open_) + by("content-naming", open_) + by("design-exploration", open_) + by("other-ux", open_)
        out += section("Accessibility, content, design", mid, cap=20)
        out += section("Research and discussion", by("research-ia", open_))
        out += section("Housekeeping", by("housekeeping", open_))
    watch_rows = sorted([r for r in watch if r["lane"] != "story-review"], key=lambda r: r["updated"], reverse=True)
    out += section("Watch (claimed by others)", watch_rows, cap=12)
    if canvas:
        lanes = {}
        for r in canvas:
            lanes[r["lane"]] = lanes.get(r["lane"], 0) + 1
        out += ["## Canvas (own design team; ask in #ai-ux before picking)", "",
                f"{len(canvas)} open items: " + ", ".join(f"{k} {v}" for k, v in sorted(lanes.items()))
                + f". [Queue](https://git.drupalcode.org/project/canvas/-/issues/?label_name%5B%5D=Needs%20design); `--tsv` lists them.", ""]
    out += ["## How to act", "",
            "- Claim: comment what you will do and when (\"ETD Friday\"), assign yourself.",
            "- Story review → guide/04-story-review.md; the ai-ux-story-review skill builds the protocol and drafts the write-up.",
            "- UX review request → answer on the requesting issue within 3 business days, guide/05-answer-a-ux-review-request.md.",
            "- Other findings → one ai_demo or module issue per finding, guide/06-file-a-ux-issue.md.",
            "- Complex or cross-module → bring to the Monday UX meeting issue above.",
            "- Every post carries the AI disclosure block (guide/07-etiquette-and-policy.md). Nothing here posts for you.", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lite", action="store_true", help="requests + story reviews + meeting only (3–4 fetches)")
    ap.add_argument("--tsv", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sprint", type=int, help="skip detection")
    ap.add_argument("--include-terminal", action="store_true", help="keep fixed/closed/postponed/blocked/inProgress/rtbc")
    args = ap.parse_args()
    today = dt.date.today()

    current, probe = detect_sprint(today, args.sprint)
    current_label = f"2026Sprint{current}"
    items, projects = collect(current_label, args.lite)
    rows = []
    for it in items.values():
        it["lane"] = lane_for(it)
        it["signals"] = signals(it, current_label, today)
        it["sources"] = sorted(it["sources"])
        if not args.include_terminal and any(s.startswith("terminal:") for s in it["signals"]):
            continue
        if args.lite and it["lane"] not in ("story-review", "review-request"):
            continue
        rows.append(it)
    rows.sort(key=lambda r: (LANES.index(r["lane"]), "unclaimed" not in r["signals"], "sprint" not in r["signals"], r["project"], r["iid"]))
    mtg = meetings(today)

    if args.json:
        json.dump({"today": today.isoformat(), "sprint": {"current": current, "label": current_label,
                   "probe": [{"n": n, "group": g, "ai": a} for n, g, a in probe]}, "lite": args.lite,
                   "projects": sorted(projects), "items": rows,
                   "meetings": {k: {"date": d.isoformat(), "iid": r["iid"], "title": r["title"],
                                    "url": f"{GL}ai_initiative/-/issues/{r['iid']}", "description": r.get("description") or ""}
                                for k, (d, r) in mtg.items()}}, sys.stdout, indent=1, default=str)
        return
    if args.tsv:
        print(f"# sprint={current_label} items={len(rows)} today={today} lite={args.lite}")
        print("lane\tref\tsignals\tlabels\tupdated\ttitle\turl")
        for r in rows:
            print("\t".join([r["lane"], r["ref"], ",".join(r["signals"]), ",".join(r["labels"]) or "-", r["updated"], r["title"], r["url"]]))
        return
    print(report(rows, current, probe, mtg, today, args.lite))


if __name__ == "__main__":
    main()
