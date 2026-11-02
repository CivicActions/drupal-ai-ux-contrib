---
name: ai-ux-radar
description: Finds design, UX, content-design, and accessibility work in the Drupal AI Initiative on git.drupalcode.org and ranks it for a designer or UX practitioner. Loads when the user invokes it by name (ai-ux-radar), asks what UX or design work the initiative needs, what to pick up as a designer this week, which Needs UX review requests are waiting, or what is on the Monday AI UX meeting. Read-only against GitLab, anonymous API, no local Drupal, no glab. Reports in chat; writes a UX-RADAR-<date>.md file only when asked.
---

# AI UX Radar

Scan the Drupal AI Initiative queues for work a designer, researcher, content designer or accessibility reviewer can take, score it against the team profile, and report it by lane. Read-only: the only write is an optional report file the user explicitly asks for. The user posts on GitLab; this skill never does.

References: [reference/lanes.md](reference/lanes.md) (lane rules, scoring, routing), [reference/queries.md](reference/queries.md) (every API call as a literal curl, for clients without the script), [reference/profile.md](reference/profile.md) (team profile; edit this, nothing else).

## Procedure

### 0. Orient

1. Read `reference/profile.md`. Missing → every fit score is 2 and say so in the report.
2. Locate the fetcher: `scripts/ux_radar.py` next to the kit (`../../scripts/ux_radar.py` relative to this file, or `scripts/ux_radar.py` in the project when the skill was installed with `--copy`). Needs `python3` only. Absent, or no shell → use the curl twins in queries.md, one call per section; every URL is literal so a chat client with web access can fetch them.
3. Today's date decides the "next Monday meeting" and request ages.

### 1. Fetch (one command)

```bash
python3 scripts/ux_radar.py
```

Prints: a `# sprint` line (detected sprint from the profile baseline, rollover flag), a `# projects` line, a TSV of candidates `lane, ref, flags, labels, updated, title, url`, then the next and previous `Drupal AI UX meeting` issues with their notes. Add `--json` for machine use, `--sprint NN` to override the baseline, `--include-terminal` to see items labelled fixed/closed/postponed/blocked/inProgress/rtbc (dropped by default: done, or someone's work).

Rollover `yes` → tell the user to bump `sprint:` in profile.md. `S<N>:ai=0` for every probe → sprint undetermined; report with that caveat.

Budget: one script run, or ≤ 12 curl calls. Never one call per issue. Do not open issue pages to "check" candidates; the TSV carries labels, assignees and dates.

### 2. Classify

The script assigns a lane (story-review, review-request, accessibility, design-exploration, content-naming, research-ia, housekeeping, other-ux) by the rules in lanes.md. Reassign when the title plainly says otherwise, and say so. Items flagged `claimed:<user>` go to **Watch** unless the user is one of the profile's GitLab usernames (then **Yours**); so do `ask-first` items (Canvas has its own design team; say to ask in `#ai-ux`). `novice` items are dropped when the profile says to skip them. `ux-request-age` is days since the request was last updated, the SLA proxy.

### 3. Score

Per candidate, /10, arithmetic shown, e.g. `8/10 (fit 3 · access 3 · urgency 2 · effort 0)`:

| Axis | Points |
|---|---|
| Fit 0–4 | lane matches a checked skill in profile.md: research/IA → research 4, story-review → research 3 + content 1, review-request → interaction 3, content-naming → content design 4, accessibility → a11y 4, design-exploration → interaction/visual 3–4, housekeeping → 2. Minus 1 when the item needs reading PHP/YAML and familiarity ≤ 1 |
| Access 0–3 | reproducible on a Drupal Forge demo instance (anything in `ai_demo`, or a path under the demo's enabled modules) = 3; screenshots or text in the issue suffice = 2; needs a specific module not on the demo = 1; needs a local Drupal or an MR checkout = 0 |
| Urgency 0–2 | `Needs UX review` with `ux-request-age` > 3 days and no reply = 2; on the current sprint, or listed under "Next story reviews"/"Next Steps" in the meeting notes = 1 |
| Effort 0–1 | bounded (one screen, one label set, one story) = 1; META/plan/cross-module = 0 |

Ties: more recent `updated`, then project name, then iid.

### 4. Report (chat)

Sections in this order, each present ("none found" when empty), every link `https://git.drupalcode.org/project/<name>/-/issues/<iid>`:

1. **This Monday's UX meeting** — date, link, agenda if any; from the previous notes: open "Next Steps" owners, "Next story reviews", decisions worth knowing.
2. **Sprint** — detected label, counts, rollover flag.
3. **Yours** — items assigned to a profile username.
4. **Story reviews** — unclaimed first, with score and the story path when known.
5. **UX review requests** — oldest unanswered first; say the SLA (3 business days) status.
6. **Design, content, accessibility** — top 5 across those lanes, score and one-line why.
7. **Research and discussion** — METAs and plans worth a comment or a sketch.
8. **Housekeeping** — docs and notes-to-issues work.
9. **Watch** — claimed items worth following.

End with routing per lanes.md: how to claim (comment with an ETD, assign yourself), where to post (story findings → `ai_demo`; request answers → the requesting issue; complex → the meeting issue), and the disclosure block reminder. Point to the guide pages: `guide/04-story-review.md`, `guide/05-answer-a-ux-review-request.md`, `guide/06-file-a-ux-issue.md`.

### 5. Write (only on request)

When the user asks for a file (`--write`, "save this", "write the radar"), write `UX-RADAR-<YYYY-MM-DD>.md` in the current directory with the same sections, a generation line (date, sprint label, item count), and the point-in-time caveat. Never commit.

## Edge cases

- 429 → wait once per `Retry-After`, rerun, flag partial data if it persists.
- Labels drift (the census in queries.md shows which variants are live). A scan returning 0 story reviews and 0 requests is more likely a label change than an empty queue; say so.
- `state::fixed`/`closed`/`postponed` on an open issue means done. `blocked`/`inProgress` means someone's work.
- Meeting notes live in the issue **description**, not comments. The next meeting's issue is usually empty until the call.
- drupal.org links 404; GitLab may redirect `/-/issues/` to `/-/work_items/`; same page.
