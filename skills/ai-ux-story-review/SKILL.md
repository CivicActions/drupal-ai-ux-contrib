---
name: ai-ux-story-review
description: Plans and writes up a usability review of an AI demo story for the Drupal AI Initiative. Loads when the user invokes it by name (ai-ux-story-review), has claimed or wants to claim an ai_demo "UX review: … story" issue, asks for a review protocol or board outline for a demo story, or has findings from a story walkthrough and wants the summary comment and follow-up issues drafted in the format the UX track uses. Drafts only; the user posts. Works in any client; plan mode fetches one issue, report mode fetches nothing.
---

# AI UX Story Review

**Plan** turns a review issue (and the story page, when the reviewer has a demo instance) into a protocol and a board outline. **Report** turns the reviewer's findings into what the UX track expects: a summary comment, one `ai_demo` issue bundling UI changes, one for story-text fixes, one per demo bug. All drafts; the person reads, edits, ticks the disclosure box, posts. Nothing here writes to GitLab.

Optional reference: [reference/protocol.md](reference/protocol.md) holds the full task questions and feature-specific Task 3 banks (chat, image, translation, validation, automators, search). Use it when the review issue is silent on Task 3; say the questions are the kit's suggestion, not the maintainer's.

## Plan mode

Trigger: a review issue URL or iid, or "I'm reviewing the <name> story".

1. Fetch the issue: `https://git.drupalcode.org/api/v4/projects/project%2Fai_demo/issues/<iid>` (JSON; `title`, `description`). It carries Goal, Before you start, Task 1–3, How to report problems, Done when. Its Task 3 is the maintainer's ask; use it verbatim.
2. If the user gives a story URL on their demo instance and a shell exists: `python3 scripts/story_steps.py <url>` prints the headings, numbered steps, screenshot alt text and links. Otherwise the steps come from the walkthrough.
3. Write the protocol: the issue's tasks, one line per story step to tick, plus the context questions the issue needs (Drupal experience; language variety for translation stories). Add the Task 4 the track expects: sketch the top two or three problems.
4. Write the board outline (below) pre-filled with the steps and the Task 3 questions.
5. Remind: comment the board link on the issue and assign yourself before starting; log out for Task 1; screenshot every step of Task 2.

Board outline:

```
UX review — <story> — <reviewer>, <date>. Context: Drupal experience <none/some/much>; <language or domain notes>. Instance started <date>.
1. Story read-through (logged out): what it does in one sentence; why an editor cares; unclear words (quoted); the problem it solves for me / how I solve it today / other products
2. Walkthrough, one frame per step: could I do it, what I clicked, screenshot; instructions visible?; result matches the story screenshot?; unclear labels or dialogs (exact text)
3. Feature questions from the issue
4. Findings, ranked: | # | Severity 1–4 | What happened | Path | Who it affects | Evidence frame | UI change or story text? |
5. Low-fidelity exploration for the top 2–3: annotated crop or sketch + the one-line change
6. Open questions for the Monday meeting
Done when: findings for every task are here; each demo bug has its own ai_demo issue linked to the review; a comment on the review issue gives the 3 most important problems and the story changes; you can show this on Monday.
```

## Report mode

Trigger: the reviewer pastes or links findings, or says "write up the review".

1. Collect once: review issue iid; board and deck links; reviewer name as credited; Drupal experience; severity per finding on the 1–4 Nielsen Norman scale (4 = usability catastrophe; a range such as "1 to 4" is fine, say whose rating); which findings have slides; anything raised on the Monday call that is not in the deck.
2. Split: **UI changes** (controls, layout, labels on screens, icons, scroll, contrast); **story text** (paths, wording, step order, screenshots that no longer match, technical depth); **feature quality** (answer correctness, model output) only when the review issue asks; **demo bugs**, one issue each; **module screens** (a contrib admin page, not the demo) stay in the summary comment flagged "module screen, maintainers will move it".
3. Draft the artefacts below, in order. Each opens with the disclosure block, Reviewed-by-a-person pre-ticked, and a line telling the reviewer to change it if they verified everything themselves.
4. Check: every table row has a severity and a slide link where one exists; no finding in two issues; the story issue references the UI issue; quoted paths are exact; no drupal.org links; cross-references use `#<iid>+s` (GitLab renders title and state).
5. Hand over: comment → the review issue; issues → `ai_demo` New issue, Task template, labels left to maintainers; add a line to the next Monday meeting issue's agenda if it is open.

### Disclosure block (every artefact)

```
<details>
<summary>

**AI disclosure**: how this issue was written

</summary>

- [ ] **Verified by a person:** I reviewed the whole issue and confirmed every step, result and claim myself.
- [x] **Reviewed by a person:** I read the issue and believe it is accurate, but did not verify every detail.
- [ ] **AI-generated:** an AI agent wrote this issue, and no person has reviewed it yet.

See the [policy on the use of AI when contributing to Drupal](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/policy-on-the-use-of-ai-when-contributing-to-drupal).

</details>
```

### 1. Summary comment (on the review issue)

```
<disclosure block, "this comment">
Review done on a Drupal Forge instance started <date>. Reviewer context: <experience; language notes>.
Findings: [board](<url>), [presentation](<url>).
**Three most important problems**  1. <what the user could not do; path; slide>  2. …  3. …
**Story changes recommended**  - <fix>, see #<story iid>+s
**Could not judge / could not confirm**  - <item, why>
Follow-ups filed: UI changes #<iid>+s, story text #<iid>+s, demo bugs #<iid>+s. Bringing the deck to the UX meeting on <date>.
```

### 2. UI changes issue — title `<Story>: UI changes from the story review (<three or four nouns>)`

```
<disclosure block>
## Summary
<Reviewer> reviewed the <story> story (#<review iid>+s) against <heuristics> and presented the findings on the <date> UX call. This issue bundles every UI change from the review and the discussion. Story text changes are a separate issue.
Full review: [presentation](<url>) and [design file](<url>). Severity is <reviewer>'s, on a 1 to 4 scale (4 is a usability catastrophe).
## Findings
| # | Change | Severity | Slide |
|---|--------|----------|-------|
| 1 | **<Imperative change.>** <What happens now, why it hurts, what to do.> | <n> | [<slide>](<url>) |
## Discussion on the call   (only if there was one: options raised and by whom, rejected and why, agreed)
## Proposed resolution
1. <design step, owner, target call>  2. <review on the UX call>  3. <build; split into child issues if needed>  4. <plain bugs that can proceed now, by number>
## Remaining tasks
- [ ] <sketches posted (owner)>  - [ ] <design review>  - [ ] <small fixes>  - [ ] <implement agreed direction>  - [ ] <re-run the story and update screenshots (story issue)>
## Related issues
- #<review iid>+s (the review)  - Story text changes: #<iid>+s
```

### 3. Story text issue — title `<Story> story: <fixes>, then re-run after the UI changes`

```
<disclosure block>
## Summary
Changes to the text of the <story> story page, from <reviewer>'s review (#<review iid>+s). <What is already good, one sentence.> <N> things need fixing, and the story needs a re-run once the UI changes land.
**Blocked by #<ui iid>+s.** The UI changes will alter labels, buttons and screenshots, so the story is updated once, after them. The quick fixes below are not blocked.
## Problems
1. **<Step N directions do not match the site.>** <Quote the step's path; what the site shows.> Slides: [<title>](<url>).
2. **<Too technical / unclear wording.>** <Who loses the thread, where.>
## Proposed resolution
- <exact correction>  - <rewrite or mark optional>  - After #<ui iid>+s: re-run end to end, replace screenshots, update steps naming changed controls.
## Remaining tasks
- [ ] <fix now (not blocked)>  - [ ] Wait for #<ui iid>+s  - [ ] Re-run and update screenshots and labels  - [ ] Ask a non-technical reader to follow the updated story once
## Related issues
- #<review iid>+s (the review)  - #<ui iid>+s (UI changes, blocks this issue)
```

### 4. Demo bug (one per bug)

First line `Found during #<review iid>+s`, then Problem (module or demo instance date, path, role), Steps with result and expected, Evidence, Proposal. Template: `templates/ux-issue.md`.

## Edge cases

- No Figma: the Slide column holds board-frame or doc-anchor links.
- A finding the reviewer could not reproduce twice goes under "Could not confirm", not in the table.
- The review issue has no Task 3: use the matching bank in `reference/protocol.md` and say so.
