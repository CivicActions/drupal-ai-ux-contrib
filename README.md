# Drupal AI UX contributor kit

Onboarding guide and two agent skills for designers and UX practitioners joining the [Drupal AI Initiative](https://new.drupal.org/ai). No local Drupal, no configuration, no login: the skills read the public git.drupalcode.org API anonymously and draft text for you to post. Nothing here writes to GitLab or Slack.

## Start here

1. Read [guide/01-where-designers-fit-in.md](guide/01-where-designers-fit-in.md), then work through [guide/02-first-week.md](guide/02-first-week.md).
2. Run the radar in newcomer mode (below). It opens with a short list of good first picks and a finished review to read before you do your own.
3. Pick a story review or a `Needs UX review` request and follow the matching how-to in `guide/`. For a story review, the `ai-ux-story-review` skill builds the protocol and drafts the write-up.

## What the radar is

The initiative's work is spread over hundreds of open issues in a dozen GitLab projects. UX work is labelled inconsistently (`Needs UX review`, `needs ux review`, `what::ux`, `ux`, `ui`, `accessibility`, `Needs design`) or not at all, and no page says "a designer is needed here". The radar is that page, generated on demand.

It is one Python script, [scripts/ux_radar.py](scripts/ux_radar.py), standard library only, plus a skill file, [skills/ai-ux-radar/SKILL.md](skills/ai-ux-radar/SKILL.md), that tells an AI assistant how to run it and how to answer questions from the result. Each run, ten to fifteen seconds:

1. Detects the current two-week sprint label (`2026SprintNN`) from the live API.
2. Fetches open issues: every `Needs UX review` request on the whole instance, the AI demo queue, the current sprint, and the UX-scoped labels on initiative projects.
3. Sorts each issue into a lane and attaches signals. There is no score and no personal profile; everyone on the team sees the same report.
4. Prints one markdown report. The assistant presents it as is and answers your question from it.

### The report

| Section | What it holds |
|---|---|
| This Monday's UX meeting | Next meeting date and link; from the previous meeting's notes: decisions, open questions, next steps with owners |
| Good first picks, Before you pick | Newcomer mode only, see below |
| Story reviews | Usability reviews of AI demo stories, unclaimed first. They run on a free Drupal Forge instance |
| UX review requests | `Needs UX review` requests, oldest first, with age in days. The track promises acknowledgement within 3 business days |
| Accessibility, content, design | Findings and fixes on module admin screens: contrast, wording, labels, dialogs, filters |
| Research and discussion | METAs and plans worth a comment or a sketch; not for assigning yourself |
| Housekeeping | Documentation and meeting-notes tasks in `ai_initiative` |
| Watch | Items claimed by others, and the Canvas queue (its own design team; ask in `#ai-ux` first) |
| How to act | How to claim, where each lane's findings go, the AI disclosure reminder |

### Lanes

| Lane | What it means for you |
|---|---|
| story-review | Walk through one demo story as a first-time visitor, log findings, sketch the top fixes. The best first task; no Drupal install |
| review-request | A maintainer asked the UX track for an opinion. Answer in a comment within three business days |
| accessibility | WCAG, contrast, keyboard, screen-reader items on module screens |
| content-naming | Labels, help text, icons, descriptions, wording |
| design-exploration | Layout, dialogs, filters, menus; `Needs design` items |
| research-ia | Plans, METAs, information architecture; comment, do not assign |
| housekeeping | Docs and notes-to-issues work; a good way to learn the landscape |

### Signals

Shown per item in place of a score: `unclaimed` or `claimed:<user>`; `forge` (reproducible on a demo instance); `sprint` (on the current sprint); `age:<n>d` (how long a request has waited); `novice` (maintainers' starter label, mostly code); `ask-first` (Canvas); `starter:<why>` (passes the newcomer rules). An open issue whose labels say `fixed`, `rtbc`, `inProgress` or `blocked` is hidden: done, or someone's work.

### Newcomer mode

New to Drupal or the initiative? Add `--starter` in the terminal, or tell the assistant "I'm new, where do I start". The report then opens with:

- **Good first picks**, up to eight: unclaimed, no merge request in flight, no METAs, not Canvas, each with one line of why (a story review on a free demo instance; a request wanting a designer's opinion; a writing task; one admin screen with one finding).
- **Before you pick**: the most recent finished story review to read first, the demo stories META, the first-week checklist, saying hello in `#ai-ux` and asking for a buddy, the glossary.

### Explain an issue

Paste any issue link and ask the assistant to explain it. It fetches that one issue, says in plain words what is asked, decodes the labels (sprint, state, lane), names who is on it, and says what a designer can do there and where the finding would go. It offers to draft the comment; you post it.

### Questions to ask the assistant

- "What UX work does the initiative need this week?"
- "I'm new to Drupal. Where do I start?"
- "Which UX review requests have waited longest?"
- "What was decided at Monday's UX meeting, and what is on the next one?"
- "I do content design. What is there for me?"
- "Explain https://git.drupalcode.org/project/ai_context/-/issues/3586662"

### What it does not do

It does not post, assign, label, or remember anything between runs. It needs no account and no configuration. The report is a point-in-time view; labels on GitLab lag, so recheck an issue before claiming it.

## The radar, three ways

| You have | Do this | You get |
|---|---|---|
| A terminal (any OS with `python3`) | `python3 scripts/ux_radar.py` (add `--starter` when new) | the full report, ten to fifteen seconds, no AI needed |
| An AI client with a shell: Claude Code, the Claude desktop app's Code tab, VS Code Copilot agent mode, Codex | `./scripts/install.sh --client claude\|copilot\|codex\|all <project-dir>` once, then say "run the UX radar" | the full report plus answers to your questions about it, newcomer mode, issue explanations |
| A chat client with URL fetch only (claude.ai, ChatGPT, Copilot Chat) | paste [skills/ai-ux-radar/SKILL.md](skills/ai-ux-radar/SKILL.md) and say "run the lite scan" | requests, story reviews and this Monday's meeting, newcomer picks from those, issue explanations; the sprint-wide accessibility, content and design lanes need the full scan |

`<project-dir>` can be this checkout. The install script symlinks by default; `--copy` for clients that do not follow symlinks. Other flags: `--lite` (the three-fetch scan from a terminal), `--tsv` and `--json` (every candidate, for filtering), `--sprint NN` (skip detection), `--include-terminal` (show hidden done or in-progress items).

## The story-review skill

`ai-ux-story-review` works in every client, including by paste. Plan mode reads one review issue and writes the protocol and board outline. Report mode turns your findings into the summary comment and follow-up issues in the shape the UX track uses. It fetches at most one issue and never posts. The human version of the method is [guide/04-story-review.md](guide/04-story-review.md).

## Layout

```
guide/                         onboarding guide, one page per topic
templates/                     intro message, story-review board, review response, UX issue body
skills/ai-ux-radar/SKILL.md    self-contained; full scan via the script, lite scan via three URLs, newcomer mode, issue explainer
skills/ai-ux-story-review/     SKILL.md with the report formats inline; reference/protocol.md has the question banks
scripts/ux_radar.py            the radar: detects the sprint, fetches, classifies, prints the report (stdlib only)
scripts/story_steps.py         prints a demo story page as markdown steps
scripts/install.sh             installs both skills into a project for Claude Code, Copilot, Codex
.github/prompts/               Copilot prompt adapters
PLAN.md                        research findings, design decisions, phases, ideas not yet built
```

## Maintenance

- Labels on git.drupalcode.org drift. The census commands are in the docstring of `scripts/ux_radar.py`; run them monthly and adjust `REQUEST_LABELS` / `SCOPED_LABELS`.
- Sprint detection probes upward from a date estimate anchored at Sprint 21 (2026-11-02, two-week cadence). If the cadence changes, update `SPRINT_ANCHOR`.
- The newcomer rules are `starter_reason()` in the script and the matching list in the skill; change both together.
- The canonical UX documentation is the AI module docs: https://project.pages.drupalcode.org/ai/1.4.x/ux/how_to_contribute/. Link to it; do not copy it here.
- Issue links are `https://git.drupalcode.org/project/<name>/-/issues/<iid>`; drupal.org issue URLs 404 since the platform migration.

## Status

See [PLAN.md](PLAN.md). Guide, templates, both skills and the radar's newcomer mode are in place. The lite scan has not yet been confirmed in a web chat client. No license yet.
