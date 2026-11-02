---
name: ai-ux-radar
description: Finds design, UX, content-design and accessibility work in the Drupal AI Initiative on git.drupalcode.org and presents it by lane for a designer or UX practitioner. Loads when the user invokes it by name (ai-ux-radar), asks what UX or design work the initiative needs, what to pick up as a designer this week, which Needs UX review requests are waiting, or what is on the Monday AI UX meeting. Zero configuration, read-only, anonymous API, no local Drupal. Works with a shell (full scan) or with URL fetch only (lite scan).
---

# AI UX Radar

Show a designer what the Drupal AI Initiative needs from them this week. Read-only: nothing here posts to GitLab or Slack; the person does that. No configuration file; every run is the same for everyone on the team.

## Full scan (any client with a shell)

```bash
python3 scripts/ux_radar.py
```

The script lives next to this skill (`../../scripts/ux_radar.py` from this file, or `scripts/ux_radar.py` in the project when installed with `--copy`). Stdlib only, about ten seconds. It detects the current sprint, fetches, classifies, and prints the finished markdown report. Present that report; do not rebuild it. Then answer the user's question (what to pick up, what is on Monday, what is unclaimed) from it. If the user names a lane or skill ("I do content design", "accessibility only"), lead with that section.

Flags: `--lite` (below), `--tsv`, `--json`, `--sprint NN` to skip detection, `--include-terminal` to show items whose labels say fixed/closed/postponed/blocked/inProgress/rtbc (hidden by default: done, or someone's work).

## Lite scan (no shell, URL fetch only)

Fetch these three URLs, then build the report sections 1–3 below from the JSON (title, labels, assignees, updated_at, web_url, description):

1. Open UX review requests, instance-wide: `https://git.drupalcode.org/api/v4/groups/project/issues?state=opened&labels=Needs%20UX%20review&per_page=50`
2. Open story reviews in the demo queue: `https://git.drupalcode.org/api/v4/projects/project%2Fai_demo/issues?state=opened&search=UX%20review&in=title&per_page=50`
3. The UX meeting issues, newest last: `https://git.drupalcode.org/api/v4/projects/project%2Fai_initiative/issues?search=UX%20meeting&in=title&state=opened&per_page=100&order_by=created_at&sort=asc`; pick the first title dated today or later as "next" and the last dated before today as "previous"; the notes are in `description`.

Say that it is a lite scan: it misses accessibility, content and design items on the sprint, which need the full scan. Do not fetch the sprint label listings (`labels=2026Sprint…`); they are 800 KB per page.

## Report

Sections, in this order, every one present ("none found" when empty). Links are `https://git.drupalcode.org/project/<name>/-/issues/<iid>`, never drupal.org.

1. **This Monday's UX meeting** — next meeting date and link; from the previous meeting's notes: Next story reviews, Decisions, Questions, Next Steps with owners.
2. **Story reviews** — unclaimed first. These run on a free Drupal Forge demo instance; no Drupal install.
3. **UX review requests** — oldest first with age in days. The track's promise is acknowledgement within 3 business days.
4. **Accessibility, content, design** — full scan only.
5. **Research and discussion** — METAs and plans worth a comment or sketch. Full scan only.
6. **Housekeeping** — docs, notes-to-issues. Full scan only.
7. **Watch** — claimed items, and Canvas items (`ask-first`: that project has its own design team; ask in `#ai-ux` before picking).
8. **How to act** — claim by commenting an ETD and assigning yourself; where each lane's findings go; the disclosure block reminder.

Signals shown per item instead of a score: `unclaimed` / `claimed:<user>`, `forge` (reproducible on a demo instance), `sprint` (on the current sprint), `age:<n>d` (request age), `novice`, `ask-first`.

## Lanes

| Lane | How an item gets there | Where findings go |
|---|---|---|
| story-review | `ai_demo` issue titled `UX review: … story`, or a first-impression test | summary comment on the review issue; one `ai_demo` issue per UI finding; `guide/04-story-review.md`, `ai-ux-story-review` skill |
| review-request | label `Needs UX review` | answer on the requesting issue; complex → Monday meeting; `guide/05-answer-a-ux-review-request.md` |
| accessibility | label `accessibility`, or WCAG/contrast/keyboard/screen-reader wording | issue or comment with the proposal; `guide/06-file-a-ux-issue.md` |
| content-naming | label/wording/help text/icon/description wording | same |
| design-exploration | label `Needs design`, or UI/layout/dialog/filter/menu wording | same |
| research-ia | `category::plan`, `[Meta]`, roadmap, journey | comment or child issue; do not assign METAs |
| housekeeping | `ai_initiative` docs and meeting-notes tasks | as the issue says |

## Edge cases

- Labels lag: an open issue labelled `fixed` or `rtbc` is done. `blocked` / `inProgress` is someone's work.
- A scan with zero story reviews and zero requests is more likely a label change than an empty queue; say so and point at the label census in the script's docstring.
- 429: wait once per `Retry-After`, rerun, flag partial data.
- The next meeting's issue is usually empty until the call; the notes you want are in the previous one.
- GitLab may redirect `/-/issues/` to `/-/work_items/`; same page.
