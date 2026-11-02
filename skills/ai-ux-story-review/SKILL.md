---
name: ai-ux-story-review
description: Plans and writes up a usability review of an AI demo story for the Drupal AI Initiative. Loads when the user invokes it by name (ai-ux-story-review), has claimed or wants to claim an ai_demo "UX review: … story" issue, asks for a review protocol or board outline for a demo story, or has findings from a story walkthrough and wants the summary comment and follow-up issues drafted in the format the UX track uses. Drafts only; the user posts. Pairs with ai-ux-radar, which finds the review issues.
---

# AI UX Story Review

Two modes. **Plan** turns a review issue (or a story page) into a protocol and a board outline before the walkthrough. **Report** turns the reviewer's findings into the three artefacts the UX track expects: a summary comment on the review issue, one `ai_demo` issue bundling UI changes, and one `ai_demo` issue for story-text fixes. Everything is a draft for the person to read, edit, tick the disclosure box, and post. Nothing here writes to GitLab.

References: [reference/protocol.md](reference/protocol.md) (task questions, feature-specific Task 3 banks, done-when checklist), [reference/report-formats.md](reference/report-formats.md) (exact shapes of the comment and issues, severity scale, cross-reference syntax).

## Plan mode

Trigger: a review issue URL or iid, or a story page URL, or "I'm reviewing the <name> story".

1. **Read the issue** (anonymous API, one call): `curl -s "https://git.drupalcode.org/api/v4/projects/project%2Fai_demo/issues/<iid>" | jq -r '.title, .description'`. It carries Goal, Before you start, Task 1–3 and Done when. Use its Task 3 verbatim when present; it is the maintainer's ask.
2. **Read the story page** when the user has a demo instance running: `python3 scripts/story_steps.py <story-url>` prints the headings, numbered steps, screenshots' alt text and links as markdown (stdlib only; works on any HTML). Without an instance, skip and say the steps come from the walkthrough.
3. **Write the protocol**: the issue's tasks, with the feature-specific question bank from protocol.md added only where the issue is silent. One line per step from the story page so the reviewer can tick them. Ask the reviewer the context questions the issue needs (Drupal experience; language variety for translation stories).
4. **Write the board outline** from `templates/story-review-board.md`, pre-filled with the story's steps and the issue's Task 3 questions. Severity scale 1–4 (report-formats.md).
5. **Remind**: comment the board link on the issue and assign yourself before starting; log out for Task 1; take a screenshot at every step of Task 2; sketch the top two or three problems (the track's rule: reviews pair with low-fidelity exploration).

## Report mode

Trigger: the reviewer pastes or links findings (board export, notes, a table), or says "write up the review".

1. **Collect**: review issue iid, board/deck links (Figma proto and design-file URLs if both exist), reviewer name as they want it credited, Drupal experience, severity per finding (1–4; ask once if missing), which findings have slides, and anything raised on the Monday call that is not in the deck.
2. **Split findings** into: UI changes (anything about controls, layout, labels on screens, icons, scroll, contrast), story text (paths, wording, step order, screenshots that no longer match, technical depth), feature quality (answer correctness, model output, speed) which gets its own issue only when the review issue asks for it, and demo bugs (each its own `ai_demo` issue, linked to the review).
3. **Draft, in this order**, using report-formats.md exactly:
   - the **summary comment** for the review issue: board links, the three most important problems, story recommendations, what the reviewer could not judge;
   - the **UI changes issue**: Summary (who reviewed what, against which heuristics, where presented), Findings table `# | Change | Severity | Slide`, Discussion (only if there was a call), Proposed resolution, Remaining tasks, Related issues;
   - the **story-text issue**: Summary with `Blocked by #<ui-iid>+s` when UI changes will alter labels or screenshots, Problems numbered, Proposed resolution, Remaining tasks (mark which are not blocked), Related issues;
   - **demo bug issues**, one each, using `templates/ux-issue.md`.
   Every artefact opens with the AI disclosure block with the **Reviewed by a person** box pre-ticked and a line telling the reviewer to change it if they verified everything themselves.
4. **Check** before handing over: every finding in the table has a severity and, where a slide exists, a link; no finding appears in two issues; the story issue references the UI issue; paths quoted from the story are exact; no drupal.org links.
5. **Hand over**: say what to post where (comment → review issue; issues → `ai_demo` New issue, Task template, labels left to maintainers) and to bring the deck to the next Monday UX meeting (`ai_initiative` meeting issue; add a line under the agenda if the issue is open).

## Edge cases

- The review issue has no Task 3: use the matching bank in protocol.md and say it is the kit's suggestion, not the maintainer's.
- The reviewer has no Figma: the Slide column holds board-frame or doc-anchor links; a plain-text board is acceptable.
- Findings about a contrib module screen (not the demo): keep them in the board and the summary comment, flag "module screen, maintainers will move it", do not file them in `ai_demo` unless the issue says to.
- A finding the reviewer cannot reproduce twice: list it under "Could not confirm" in the comment, not in the table.
