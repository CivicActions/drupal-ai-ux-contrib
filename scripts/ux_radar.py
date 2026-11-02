#!/usr/bin/env python3
"""Fetch design/UX/content/accessibility candidates from the Drupal AI Initiative queues.

Zero dependencies (stdlib only), anonymous API, read-only. Prints TSV by default.

  python3 scripts/ux_radar.py [--sprint NN] [--json] [--no-meetings] [--include-claimed]

Env: DRUPALCODE_API overrides https://git.drupalcode.org/api/v4 (fixtures/tests).
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

# Labels. Requests are instance-wide by design; the rest are kept only on initiative projects.
REQUEST_LABELS = ["Needs UX review", "needs ux review"]
SCOPED_LABELS = ["what::ux", "ux", "ui", "accessibility", "Accessibility", "Needs design"]
TITLE_KEYWORDS = re.compile(
    r"\b(UX|UI|usability|accessib\w*|WCAG|design|labels?|wording|icons?|dialogs?|modal|story|stories|"
    r"help text|naming|rename|screen ?reader|keyboard|contrast|first[- ]impression|user experience)\b",
    re.I,
)
# The demo queue is read whole; keep only rows a designer can act on.
DEMO_KEYWORDS = re.compile(
    r"\b(UX|UI|button|menu|link|page|upload|message|dialog|consent|story|stories|label|icon|text|review|"
    r"experience|feature page|screenshot|wording|instructions?)\b", re.I)
# Labels that read as done or as someone's work; dropped unless --include-terminal.
TERMINAL = {"state::fixed", "state::closed", "state::postponed", "state::blocked", "state::inProgress", "state::rtbc"}
# Projects with their own design team: flag ask-first, route through #ai-ux before picking.
ASK_FIRST_PROJECTS = {"canvas"}
MEETING_TITLE = re.compile(r"Drupal AI UX meeting (\d{1,2} \w+ \d{4})", re.I)


def get(path, params=None, want_headers=False):
    url = f"{API}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params, safe=":,[]")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            return (r.headers, json.loads(body or b"null")) if want_headers else json.loads(body or b"null")
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"warn: {e.code} {url}\n")
        return ({}, []) if want_headers else []
    except urllib.error.URLError as e:
        sys.stderr.write(f"error: {e.reason} {url}\n")
        sys.exit(1)


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


def profile_sprint():
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (
        os.path.join(here, "..", "skills", "ai-ux-radar", "reference", "profile.md"),
        os.path.join(os.getcwd(), ".claude", "skills", "ai-ux-radar", "reference", "profile.md"),
        os.path.join(os.getcwd(), ".agents", "skills", "ai-ux-radar", "reference", "profile.md"),
        os.path.join(os.getcwd(), ".github", "skills", "ai-ux-radar", "reference", "profile.md"),
    ):
        try:
            with open(cand, encoding="utf-8") as f:
                m = re.search(r"^- sprint:\s*(\d+)", f.read(), re.M)
                if m:
                    return int(m.group(1))
        except OSError:
            continue
    return None


def detect_sprint(baseline):
    """Current sprint = highest N in baseline..baseline+2 active on project ai; fallback highest with group>0."""
    rows = []
    for n in range(baseline, baseline + 3):
        label = f"2026Sprint{n}"
        g = total(f"{GROUP}/issues", {"state": "opened", "labels": label})
        a = total("projects/project%2Fai/issues", {"state": "opened", "labels": label})
        rows.append((n, g, a))
    active_ai = [n for n, g, a in rows if a >= 1]
    active_group = [n for n, g, a in rows if g >= 1]
    current = max(active_ai) if active_ai else (max(active_group) if active_group else baseline)
    return current, rows


def norm(issue, source):
    labels = issue.get("labels") or []
    return {
        "ref": issue["references"]["full"].replace("project/", ""),
        "project": issue["references"]["full"].split("#")[0].replace("project/", ""),
        "iid": issue["iid"],
        "title": issue["title"],
        "labels": labels,
        "assignees": [a["username"] for a in issue.get("assignees") or []],
        "updated": issue["updated_at"][:10],
        "created": issue["created_at"][:10],
        "url": issue["web_url"].replace("/-/work_items/", "/-/issues/"),
        "sources": {source},
    }


def lane_for(item):
    t = item["title"]
    labels_l = {l.lower() for l in item["labels"]}
    p = item["project"]
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


def flags(item, current_label, today):
    f = []
    if item["assignees"]:
        f.append("claimed:" + ",".join(item["assignees"]))
    if current_label in item["labels"]:
        f.append("sprint")
    if any(l.lower() == "needs ux review" for l in item["labels"]):
        age = (today - dt.date.fromisoformat(item["updated"])).days
        f.append(f"ux-request-age:{age}d")
    if any(l.lower().startswith("novice") for l in item["labels"]):
        f.append("novice")
    if item["project"] in ASK_FIRST_PROJECTS:
        f.append("ask-first")
    term = sorted(l for l in item["labels"] if l in TERMINAL)
    if term:
        f.append("terminal:" + ",".join(term))
    return f


def meetings(today):
    rows = get("projects/project%2Fai_initiative/issues",
               {"search": "UX meeting", "in": "title", "per_page": 100, "order_by": "created_at"})
    dated = []
    for r in rows or []:
        m = MEETING_TITLE.search(r["title"])
        if not m:
            continue
        try:
            d = dt.datetime.strptime(m.group(1), "%d %B %Y").date()
        except ValueError:
            continue
        dated.append((d, r))
    dated.sort()
    upcoming = [x for x in dated if x[0] >= today]
    past = [x for x in dated if x[0] < today]
    out = {}
    if upcoming:
        out["next"] = upcoming[0]
    if past:
        out["previous"] = past[-1]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sprint", type=int, help="baseline sprint number (default: profile.md, else 21)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-meetings", action="store_true")
    ap.add_argument("--include-claimed", action="store_true", help="keep assigned issues (default: kept, flagged)")
    ap.add_argument("--include-terminal", action="store_true", help="keep fixed/closed/postponed/blocked/inProgress/rtbc")
    args = ap.parse_args()
    today = dt.date.today()

    baseline = args.sprint or profile_sprint() or 21
    current, probe = detect_sprint(baseline)
    current_label = f"2026Sprint{current}"
    rollover = current > baseline

    items = {}

    def add(issues, source):
        for i in issues or []:
            n = norm(i, source)
            if n["ref"] in items:
                items[n["ref"]]["sources"].add(source)
            else:
                items[n["ref"]] = n

    # 1. Sprint + initiative scans: project allowlist and keyword pass.
    sprint_issues = pages(f"{GROUP}/issues", {"state": "opened", "labels": current_label})
    init_issues = pages(f"{GROUP}/issues", {"state": "opened", "labels": "AI Initiative Sprint"}, max_pages=3)
    initiative_projects = {i["references"]["full"].split("#")[0].replace("project/", "") for i in sprint_issues + init_issues}
    initiative_projects |= {"ai_demo", "ai_initiative", "ai", "ai_context", "ai_agents", "ai_ckeditor", "canvas"}
    add([i for i in sprint_issues if TITLE_KEYWORDS.search(i["title"])], "sprint-keyword")
    add([i for i in init_issues if TITLE_KEYWORDS.search(i["title"])], "initiative-keyword")

    # 2. Request labels, instance-wide.
    for label in REQUEST_LABELS:
        add(pages(f"{GROUP}/issues", {"state": "opened", "labels": label}, max_pages=1), f"label:{label}")

    # 3. Scoped labels, initiative projects only.
    for label in SCOPED_LABELS:
        rows = pages(f"{GROUP}/issues", {"state": "opened", "labels": label}, max_pages=1)
        rows = [r for r in rows if r["references"]["full"].split("#")[0].replace("project/", "") in initiative_projects]
        add(rows, f"label:{label}")

    # 4. The demo queue, whole.
    demo = pages("projects/project%2Fai_demo/issues", {"state": "opened"}, max_pages=1)
    add([i for i in demo if DEMO_KEYWORDS.search(i["title"])
         or {l.lower() for l in i.get("labels") or []} & {"ui", "ux", "needs ux review"}], "ai_demo")

    rows = []
    for it in items.values():
        it["lane"] = lane_for(it)
        it["flags"] = flags(it, current_label, today)
        if not args.include_terminal and any(f.startswith("terminal:") for f in it["flags"]):
            continue
        it["sources"] = sorted(it["sources"])
        rows.append(it)
    lane_order = ["story-review", "review-request", "accessibility", "design-exploration", "content-naming",
                  "research-ia", "housekeeping", "other-ux"]
    rows.sort(key=lambda r: (lane_order.index(r["lane"]), "sprint" not in r["flags"], r["project"], r["iid"]))

    mtg = {} if args.no_meetings else meetings(today)

    if args.json:
        json.dump({
            "sprint": {"current": current, "label": current_label, "baseline": baseline, "rollover": rollover,
                       "probe": [{"n": n, "group": g, "ai": a} for n, g, a in probe]},
            "projects": sorted(initiative_projects),
            "items": rows,
            "meetings": {k: {"date": d.isoformat(), "ref": r["references"]["full"], "url": r["web_url"].replace("/-/work_items/", "/-/issues/"),
                             "title": r["title"], "description": r.get("description") or ""}
                         for k, (d, r) in mtg.items()},
        }, sys.stdout, indent=1, default=str)
        return

    print(f"# sprint current={current} label={current_label} baseline={baseline} rollover={'yes' if rollover else 'no'} "
          + " ".join(f"S{n}:group={g},ai={a}" for n, g, a in probe))
    print(f"# projects={len(initiative_projects)} items={len(rows)} today={today}")
    print("lane\tref\tflags\tlabels\tupdated\ttitle\turl")
    for r in rows:
        keep_labels = [l for l in r["labels"] if l.startswith(("state::", "ai::", "category::", "2026Sprint", "what::"))
                       or l.lower() in {"needs ux review", "ux", "ui", "accessibility", "needs design", "novice", "documentation"}]
        print("\t".join([r["lane"], r["ref"], ",".join(r["flags"]) or "-", ",".join(keep_labels) or "-",
                         r["updated"], r["title"], r["url"]]))
    for key in ("next", "previous"):
        if key in mtg:
            d, r = mtg[key]
            desc = (r.get("description") or "").strip()
            print(f"\n## meeting {key}: {d.isoformat()} {r['references']['full']} {r['web_url'].replace('/-/work_items/', '/-/issues/')}")
            print(desc[:4000] if desc else "(no notes yet)")
            if len(desc) > 4000:
                print(f"... ({len(desc) - 4000} more chars; open the issue)")


if __name__ == "__main__":
    main()
