# 4. How to do a story review

A story is a page on the demo site explaining one AI feature and walking the visitor through trying it. A story review tests whether the story and the feature work for someone who has never seen Drupal. Reference issue: [UX review: AI Translate story](https://git.drupalcode.org/project/ai_demo/-/issues/3628683).

## Before you start

1. Start a fresh demo instance. Do not log in yet.
2. Make a board for findings in Figma, Miro or Google Docs. Set it so others can comment. Outline: [templates/story-review-board.md](../templates/story-review-board.md).
3. Comment the board link on the issue and assign yourself.

## Task 1: read the story cold

Logged out, story page only. Note: is it clear what the feature does and why an editor would care? Which words or sentences are unclear? Does it solve a problem you recognise, and how do you solve it today? What other products do this?

## Task 2: follow the story in the demo

Story and demo side by side. Do each step; log in when told. Note where you did not know what to do, whether the instructions stayed visible, whether the result matched the screenshots, which labels or screens were unclear, and any dialog or message that stopped you. Screenshot each.

## Task 3: the feature itself

The issue usually adds feature-specific questions (for Translate: can an editor trust and review the output). Answer them. Say what you could not judge.

## Task 4: low-fidelity exploration

For the two or three biggest problems, sketch a fix. Crops of the real screen with annotations are enough. This is what turns the review into work the developers can take.

## Posting

Summary in a comment on the review issue: board link, top findings, one line per sketch. File each UI change as its own `ai_demo` issue ("one row per finding with a slide link" is the format the track uses, see [06-file-a-ux-issue.md](06-file-a-ux-issue.md)). Story-text fixes go in one issue; UI changes in another, and the text issue waits for the UI one. Bring it to the next Monday meeting.
