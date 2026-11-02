# Drupal AI UX contributor kit

Onboarding guide and agent skills for designers and UX practitioners joining the [Drupal AI Initiative](https://new.drupal.org/ai). Everything here works without a local Drupal install: the skills read the public git.drupalcode.org API with plain `curl`.

## Start here

1. Read [guide/01-why-you-are-wanted.md](guide/01-why-you-are-wanted.md), then work through [guide/02-first-week.md](guide/02-first-week.md).
2. Run the radar to see what needs a designer this week (see below).
3. Pick a story review or a `Needs UX review` request from the radar and follow the matching how-to in `guide/`. For a story review, the `ai-ux-story-review` skill builds the protocol and drafts the write-up.

## Skills

| Skill | Does | Needs |
|---|---|---|
| `ai-ux-radar` | finds and ranks design, UX, content and accessibility work across the initiative; reads the Monday UX meeting notes | `curl` or `python3`, no login |
| `ai-ux-story-review` | plans a demo story review (protocol + board) and drafts the summary comment and follow-up issues in the track's format | a Drupal Forge demo instance for the walkthrough |

Both are read-only against GitLab and draft text for you to post.

## Run the radar

The `ai-ux-radar` skill scans git.drupalcode.org for design, UX, content and accessibility work in the initiative and ranks it against the team profile. Read-only; it never posts.

| Client | How |
|---|---|
| Claude Code | `./scripts/install.sh --client claude <your-project-dir>` then type `/ai-ux-radar` |
| VS Code Copilot (agent mode) | `./scripts/install.sh --client copilot <your-project-dir>` then run the `ai-ux-radar` prompt |
| Codex and other Agent Skills clients | `./scripts/install.sh --client codex <your-project-dir>` (installs to `.agents/skills/`) |
| Any chat client with web access | Paste [skills/ai-ux-radar/SKILL.md](skills/ai-ux-radar/SKILL.md) and say "run the radar" |

The install script places every skill under `skills/`, so the same commands install `ai-ux-story-review`.
| No AI client | `python3 scripts/ux_radar.py` prints the raw candidate list as TSV |

`<your-project-dir>` can be this checkout. The install script symlinks by default; add `--copy` for a client that does not follow symlinks.

## Layout

```
guide/                         onboarding guide, one page per topic
templates/                     intro message, story-review board, review response, UX issue body
skills/ai-ux-radar/            radar skill (SKILL.md + reference/)
skills/ai-ux-radar/reference/profile.md   team profile the radar scores against — edit this
skills/ai-ux-story-review/     story review skill (protocol, report formats)
scripts/ux_radar.py            zero-dependency fetcher the radar calls when present
scripts/story_steps.py         prints a story page as markdown steps for the review protocol
scripts/install.sh             installs skills into a project for Claude Code, Copilot, Codex
.github/prompts/               Copilot prompt adapter
```

## Maintenance

- Labels on git.drupalcode.org drift. Re-run the label census in `skills/ai-ux-radar/reference/queries.md` monthly and adjust the label list in `scripts/ux_radar.py`.
- Canonical UX documentation lives in the AI module docs: https://project.pages.drupalcode.org/ai/1.4.x/ux/how_to_contribute/. Link to it; do not copy it here.
- Issue links must point at `https://git.drupalcode.org/project/<name>/-/issues/<iid>`; drupal.org issue URLs 404 since the platform migration.

## Status

Phases 0–3 of [PLAN.md](PLAN.md): guide, templates, radar and story-review skills. Planned next (phase 4): weekly digest action, meeting-prep skill. No license yet.
