# Lanes, scoring, routing

## Lanes

Assigned in this order; the first rule that matches wins. The script implements the same rules (`lane_for` in `scripts/ux_radar.py`).

| Lane | Rule | Typical item |
|---|---|---|
| `story-review` | project `ai_demo` and title has `UX review:`, `story`, or `first-impression` | "UX review: AI Translate story" |
| `housekeeping` | project `ai_initiative` and docs/meeting-notes wording or label `documentation` | "Review all AI UX meeting notes … create issues" |
| `review-request` | label `Needs UX review` (any case) | "How does the provider notify of better models" |
| `accessibility` | label `accessibility`/`Accessibility`, or title has accessib*, WCAG, screen reader, keyboard, contrast | "… changes the page on input (WCAG 3.2.2): choose a fix" |
| `research-ia` | label `category::plan`, or title has `[Meta]`, `[Plan]`, META, roadmap, research, journey, information architecture, stream | "[Meta] People: CCC roadmap stream" |
| `content-naming` | title has label(s), wording, help text, naming, rename, terminology, typo, text, icon(s), description(s), instructions | "Correct the Language scope fail-open text" |
| `design-exploration` | label `Needs design`, or title has choose a fix, UI, design, sketch, mockup, wireframe, layout, dialog, modal, redesign, explorer, UX, filter, listing, sorting, button, menu, navigation, scroll | "Ask AI: UI changes from the story review" |
| `other-ux` | reached only through a UX label | token budget tiers |

The `ai_demo` queue is read whole but only rows with UI/UX wording or a `ui`/`Needs UX review` label become candidates; infrastructure bugs in the demo are not design work.

Flags on every row: `claimed:<users>`, `sprint` (current sprint label), `ux-request-age:<n>d` (days since the request was last updated; the SLA proxy), `novice`, `ask-first` (project with its own design team, currently `canvas`: route through `#ai-ux` before picking), `terminal:<labels>` (only with `--include-terminal`).

## Exclusions

- Labels `state::fixed`, `state::closed`, `state::postponed`, `state::rtbc` → done. `state::blocked`, `state::inProgress` → someone's work. Dropped unless `--include-terminal`.
- `ask-first` items (Canvas) go to **Watch** with a note to ask in `#ai-ux`; the Canvas team designs its own UI.
- `claimed:<user>` → **Watch**, unless the user is in profile.md → **Yours**.
- `novice` → dropped when profile.md says to skip novice items.
- Projects listed under profile.md "Exclusions".

## Scoring

| Axis | Points |
|---|---|
| Fit 0–4 | from profile skills: research/IA 4 (research), story-review 3 (+1 content), review-request 3 (interaction), content-naming 4 (content design), accessibility 4 (a11y), design-exploration 3–4 (interaction/visual), housekeeping 2. −1 if the item needs PHP/YAML reading and familiarity ≤ 1 |
| Access 0–3 | Drupal Forge demo reproduces it 3 · screenshots/text in the issue suffice 2 · needs a module not on the demo 1 · needs local Drupal or MR checkout 0 |
| Urgency 0–2 | `Needs UX review` older than 3 business days, unanswered 2 · current sprint label, or named in the meeting notes' Next Steps / Next story reviews 1 |
| Effort 0–1 | bounded 1 · META, plan, cross-module 0 |

Ties: newest `updated`, project name, iid.

## Routing

| Lane | Claim | Post findings | Guide |
|---|---|---|---|
| story-review | comment with board link + ETD, assign yourself | summary on the review issue; one `ai_demo` issue per UI finding; text fixes in one issue that waits on the UI issue | `guide/04-story-review.md` |
| review-request | acknowledge within 3 business days | on the requesting issue; complex → Monday meeting issue | `guide/05-answer-a-ux-review-request.md` |
| accessibility, content-naming, design-exploration | comment + assign | proposal or sketch on the issue | `guide/06-file-a-ux-issue.md` |
| research-ia | comment; do not assign METAs | findings as a comment or a child issue | `guide/03-where-the-work-is.md` |
| housekeeping | comment + assign | as the issue says | — |

Every post carries the AI disclosure block (`guide/07-etiquette-and-policy.md`). Nothing in this kit posts for you.
