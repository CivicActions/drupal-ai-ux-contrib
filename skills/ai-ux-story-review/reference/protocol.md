# Story review protocol

Source: the `ai_demo` review issues (Ask AI #3628675, AI Translate #3628683, image validation #3628684, alt text #3628681). The issue's own tasks win; use this file to fill gaps.

## Before you start (always)

1. Start a new demo instance from Drupal Forge (https://new.drupal.org/ai/demo). Do not log in yet.
2. **AI Features** button → find the story.
3. Make a board or document (Figma, Miro, Google Docs); enable comments for anyone with the link.
4. Comment the link on the review issue; assign yourself.
5. Record your context: Drupal experience; anything the issue asks (for translation: do you read the language, which variety).

## Task 1: read the story (logged out, story page only)

- Is it clear what the feature does?
- Is it clear why the feature is important for a site editor?
- Which words or sentences are not clear? Quote them.
- Does the feature solve a problem that you know? Which problem?
- How do you solve this problem now?
- Which other products do the same thing?
- (Translation stories) Is it clear why the demo chose this language variety, and that it is a prompt choice, not a model setting?

## Task 2: follow the story in the demo (side by side)

Do each step; log in when told. Screenshot every step.

- Can you do each step?
- At which step did you not know what to do?
- Can you see the story instructions while you do each step?
- Is the result the same as in the story? Compare your screen with the story's screenshots.
- Which labels or screens are not clear? Quote exact text.
- Did any dialog or message stop you? Record what it said.

## Task 3: the feature itself (banks by feature type)

**Chat / Ask AI / AI Answers.** Ask 5+ questions, each continuing from the last answer, as a student, parent or staff member would. Per answer: correct? cites site content? links open the right pages? refuses what the site cannot answer? strange, incomplete or wrong (record the exact question)? Also: can you stop a running answer; does the page scroll away; are sources readable.

**Image: alt text, focal point, classification.** Upload 5+ varied images (one person, group, building, landscape, image with text such as a poster or chart, one tall narrow image). Alt text: correct? adds details not in the image? good length? starts with "Image of"? includes important text? would you use, change or rewrite it? Focal point: on the important part? is the preview of crops clear? faster than doing it yourself? Description and tags on save: expected? correct? how many, useful? who can see them? Search by tag: can you find your image; how do you know which tags exist?

**Translation.** Translate 2–3 pages of different length. Is the translation complete? Is the variety the one the story promised? Can an editor review and correct it? Is the model choice and the prompt discoverable where the story says? Is the cost estimate understandable? Does the link text make sense to a non-developer ("Translate using chat_translation")?

**Validation / content review / guardrails.** Trigger the check with content that should pass and content that should fail. Is the message clear about what is wrong and what to do? Can you override or dismiss? Is the completion state obvious? Can you run it again?

**Automators / field actions (generate title, summary).** Run the action on 3 pieces of content. Is the result where you expected? Can you undo? Is it clear what the AI used as input? Does it run when you did not want it to (on save)?

**Search.** 5+ queries a visitor would type. Relevant? Is it clear results are AI-ranked or AI-summarised? Can you get to a normal listing?

Record the exact input and result whenever the AI gives a strange, incomplete or wrong result.

## Task 4: low-fidelity exploration (track rule)

For the top 2–3 problems: an annotated crop or sketch and the one-line change it proposes. Enough to frame a discussion, not finished designs.

## How to report problems

- Problem in the story or the demo (text, content, broken page, screenshot mismatch): a new `ai_demo` issue linked to the review issue. No approval needed.
- Problem in a module screen (a label on a contrib admin page): keep it in the findings with the module name; maintainers move it to the right queue.

## Done when

- [ ] Task 1–3 findings are on the board.
- [ ] Each demo bug has its own issue linked to the review.
- [ ] A comment on the review issue gives the 3 most important problems.
- [ ] The comment recommends changes to the story.
- [ ] You can show the findings at the next Monday UX meeting.
