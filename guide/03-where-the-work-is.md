# 3. Where the work is

Snapshot 2026-11-02; run the radar for today's list.

| Kind of work | Where | Signal |
|---|---|---|
| **Story reviews** of the AI demo | project `ai_demo` | title `UX review: … story`, label `Needs UX review`; also "first-impression test" and `[META] General UX improvements to the AI Demo` |
| **UX review requests** on any module | instance-wide | label `Needs UX review` (also lower-case `needs ux review`). Design decisions: how to notify of better models, Agents Explorer redesign, chatbot ideas META |
| **Content and naming** fixes | mostly `ai_context` | label `what::ux`; titles with "label", "wording", "text", "icon" |
| **Accessibility** | `ai_context`, `ai` | labels `accessibility`, `Accessibility`; WCAG numbers in titles; `[Meta] CCC accessibility testing` |
| **Information architecture / research** | `ai_context` People stream META (3586623), chatbot UX META (`ai_initiative` 3544476) | `category::plan`, `needs ux review` |
| **Housekeeping** | `ai_initiative` | mine meeting notes into issues (3559136), refresh UX docs (3566916), DrupalForge-testable issue guidance (3583362) |
| **Product design, heavier** | `canvas` (Canvas AI chat), AI Agents Explorer | has its own designers; ask in `#ai-ux` before picking |

Labels you will see and what they mean:

- `2026SprintNN` — in the current two-week sprint. `AI Initiative Sprint` alone is stale; ignore it as a "current" signal.
- `ai::inside` / `ai::outside` / `ai::internal` — the lane.
- `state::toBeTriaged` / `readyForWork` / `accepted` — open for pickup. `inProgress` / `blocked` — someone's work. `needsReview` / `rtbc` — awaiting review or merge. `fixed` / `closed` / `postponed` — done or parked, even if the issue is still open.
- `Needs UX review` — the UX track's request tag. Not `Needs usability review`, which is Drupal core's.
- `Novice` — marked as a starter task by maintainers.

Where findings go: story-review findings are filed in `ai_demo`; the feature modules opt in to what they want. UX review answers go on the requesting issue. Anything complex goes to the Monday meeting.
