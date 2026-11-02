# Report formats

Mirrors what the UX track posted after the first story review (Ask AI, 2026-10-26): review issue #3628675, UI changes #3628686, story text #3628687.

## Conventions

- **Severity**: 1–4, Nielsen Norman scale, 4 = usability catastrophe. A range ("1 to 4") is allowed when the impact depends on context; say whose rating it is.
- **Cross-references**: `#3628686+s` (GitLab renders title and state). Same project only; cross-project use `project/ai_context#3586623+s`.
- **Links**: `https://git.drupalcode.org/project/ai_demo/-/issues/<iid>`; never drupal.org.
- **Disclosure block** opens every artefact (collapsed `<details>`), Reviewed-by-a-person pre-ticked:

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

For a comment, use the same block with "this comment".

## 1. Summary comment on the review issue

```
<disclosure block>

Review done on a Drupal Forge instance started <date>. Reviewer context: <Drupal experience; language notes>.

Findings: [board](<url>)<, [presentation](<url>)>.

**Three most important problems**
1. <what the user could not do, one sentence; path; slide link>
2. …
3. …

**Story changes recommended**
- <path fix / wording / step order>, see <story issue #iid+s>

**Could not judge / could not confirm**
- <item and why>

Follow-ups filed: UI changes #<iid>+s, story text #<iid>+s<, demo bugs #<iid>+s …>. Bringing the deck to the UX meeting on <date>.
```

## 2. UI changes issue

Title: `<Story>: UI changes from the story review (<three or four nouns>)`. Project `ai_demo`, template Task.

```
<disclosure block>

## Summary

<Reviewer> reviewed the <story> story (#<review iid>+s) against <heuristics used> and presented the findings on the <date> UX call. This issue bundles every UI change that came out of the review<and the discussion>. The story text changes<and the answer quality work> are separate issues.

Full review: [presentation](<url>) and [design file](<url>). Severity is <reviewer>'s, on a 1 to 4 scale (4 is a usability catastrophe).

## Findings

| # | Change | Severity | Slide |
|---|--------|----------|-------|
| 1 | **<Imperative change.>** <What happens now and why it hurts, one or two sentences. What to do.> | <n> | [<slide title>](<url>) |

<## Discussion on the call — bullets per topic: options raised and by whom, what was rejected and why, what was agreed.>

## Proposed resolution

1. <design step, owner, target call date>
2. <review step>
3. <build step; split into child issues when needed>
4. <items that are plain bugs and can proceed without the design pass, by number>

## Remaining tasks

- [ ] <sketches posted (owner)>
- [ ] <design review on the UX call>
- [ ] <fix list of small items>
- [ ] <implement agreed direction>
- [ ] <re-run the story and update screenshots (tracked in the story issue)>

## Related issues

- #<review iid>+s (the review)
- Story text changes: #<iid>+s
<- Feature quality: #<iid>+s>
```

## 3. Story text issue

Title: `<Story> story: <the fixes>, then re-run after the UI changes`.

```
<disclosure block>

## Summary

Changes to the text of the <story> story page, from <reviewer>'s review (#<review iid>+s). <One sentence on what is already good.> <N> things need fixing, and the whole story needs a re-run once the UI changes land.

**Blocked by #<ui iid>+s.** The UI changes will alter labels, buttons and screenshots, so the story should be updated once, after them. The quick fixes below are not blocked.

## Problems

1. **<Step N directions do not match the site.>** <Quote the step's path; say what the site shows.> Slides: [<title>](<url>).
2. **<Too technical / unclear wording.>** <Who loses the thread and where.>

## Proposed resolution

- <exact correction>
- <rewrite or mark optional>
- After #<ui iid>+s lands: re-run end to end, replace screenshots, update any step naming a changed control.

## Remaining tasks

- [ ] <fix now (not blocked)>
- [ ] Wait for #<ui iid>+s
- [ ] Re-run the story and update screenshots and labels
- [ ] Ask a non-technical reader to follow the updated story once

## Related issues

- #<review iid>+s (the review)
- #<ui iid>+s (UI changes, blocks this issue)
```

## 4. Demo bug

One per bug, `templates/ux-issue.md`, first line `Found during #<review iid>+s`.
