# Drupal AI UX contributor kit

Onboarding guide and two agent skills for designers and UX practitioners joining the [Drupal AI Initiative](https://new.drupal.org/ai). No local Drupal, no configuration, no login: the skills read the public git.drupalcode.org API anonymously and draft text for you to post.

## Start here

1. Read [guide/01-where-designers-fit-in.md](guide/01-where-designers-fit-in.md), then work through [guide/02-first-week.md](guide/02-first-week.md).
2. Run the radar (below) to see what needs a designer this week.
3. Pick a story review or a `Needs UX review` request and follow the matching how-to in `guide/`. For a story review, the `ai-ux-story-review` skill builds the protocol and drafts the write-up.

## The radar, three ways

| You have | Do this | You get |
|---|---|---|
| A terminal (any OS with `python3`) | `python3 scripts/ux_radar.py` | the full report, about ten seconds, no AI needed |
| An AI client with a shell: Claude Code, the Claude desktop app's Code tab, VS Code Copilot agent mode, Codex | `./scripts/install.sh --client claude\|copilot\|codex\|all <project-dir>` once, then say "run the UX radar" | the full report plus answers to your questions about it |
| A chat client with URL fetch only (claude.ai, ChatGPT, Copilot Chat) | paste [skills/ai-ux-radar/SKILL.md](skills/ai-ux-radar/SKILL.md) and say "run the lite scan" | requests, story reviews and this Monday's meeting; the sprint-wide accessibility, content and design lanes need the full scan |

`<project-dir>` can be this checkout. The install script symlinks by default; `--copy` for clients that do not follow symlinks.

## The story-review skill

`ai-ux-story-review` works in every client, including by paste. Plan mode reads one review issue and writes the protocol and board outline. Report mode turns your findings into the summary comment and follow-up issues in the shape the UX track uses. It fetches at most one issue and never posts.

## Layout

```
guide/                         onboarding guide, one page per topic
templates/                     intro message, story-review board, review response, UX issue body
skills/ai-ux-radar/SKILL.md    self-contained; full scan via the script, lite scan via three URLs
skills/ai-ux-story-review/     SKILL.md with the report formats inline; reference/protocol.md has the question banks
scripts/ux_radar.py            the radar: detects the sprint, fetches, classifies, prints the report (stdlib only)
scripts/story_steps.py         prints a demo story page as markdown steps
scripts/install.sh             installs both skills into a project for Claude Code, Copilot, Codex
.github/prompts/               Copilot prompt adapters
```

## Maintenance

- Labels on git.drupalcode.org drift. The census commands are in the docstring of `scripts/ux_radar.py`; run them monthly and adjust `REQUEST_LABELS` / `SCOPED_LABELS`.
- Sprint detection probes upward from a date estimate anchored at Sprint 21 (2026-11-02, two-week cadence). If the cadence changes, update `SPRINT_ANCHOR`.
- The canonical UX documentation is the AI module docs: https://project.pages.drupalcode.org/ai/1.4.x/ux/how_to_contribute/. Link to it; do not copy it here.
- Issue links are `https://git.drupalcode.org/project/<name>/-/issues/<iid>`; drupal.org issue URLs 404 since the platform migration.

## Status

See [PLAN.md](PLAN.md). Guide, templates and both skills are in place; the lite scan has not yet been confirmed in a web chat client. No license yet.
