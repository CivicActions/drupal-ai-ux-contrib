# Plan — Drupal AI UX contributor kit

Onboarding guide + standalone `ai-ux-radar` skill for designers and UX practitioners joining the Drupal AI Initiative. This repo is the implementation. Research snapshot 2026-11-02; GitLab counts are point-in-time.

> **Revision 2026-11-02 (after the first paste test).** Pasting SKILL.md into a web chat client failed: the skill depended on sibling files, a shell, and raw API pages of 800 KB. Decisions: no team profile (fit scoring was constant for a team with all five skills), no numeric scores (signals instead), no scheduled radar, no report file. The script detects the sprint itself and prints the finished report; both SKILL.md files are self-contained; a lite scan of three URLs (~110 KB) serves clients with URL fetch only. The repo will be made public. Sections 2.1, 2.3 and 2.4 below describe the first design and are kept for the record.

## 1. Research findings

### 1.1 The initiative already has a UX track — it is just hard to find

| Entry point | What it is | Source |
|---|---|---|
| `#ai-ux` Slack channel | Where you introduce yourself; a product owner matches you to a project | [How to Contribute to UX](https://project.pages.drupalcode.org/ai/1.4.x/ux/how_to_contribute/) |
| Weekly **Drupal AI UX meeting**, Mondays | One `ai_initiative` issue per meeting, pre-created through 28 Dec 2026 (iids 3586620–3586628). Notes go in the issue description: story reviews, Figma deck links, decisions, next steps with owners. ~8 attendees on 26 Oct | [#3586619](https://git.drupalcode.org/project/ai_initiative/-/issues/3586619) |
| `Needs UX review` tag | The request mechanism. Ack within 3 business days; simple items resolved in a week; complex ones go to the Monday meeting | [Request UX Support](https://project.pages.drupalcode.org/ai/1.4.x/ux/request_ux_support/) |
| Core UX Principles | Audience = site builders/editors; naming order accuracy → site-builder friendly (no Drupalisms) → developer context in descriptions → benefit language; progressive disclosure; hierarchy over flat lists | [Core UX Principles](https://project.pages.drupalcode.org/ai/1.4.x/ux/core_ux_principles/) |
| AI UX hierarchy | Infrastructure → Tools & Automation → Features (5 subcategories); `*.links.menu.yml` parent keys `ai.admin_config_*` | [Organizing AI Modules & Features](https://project.pages.drupalcode.org/ai/1.4.x/ux/organizing_ai_modules_and_features/) |
| UX Improvement Projects | Discovery → Design (wireframes on the shared Figma board) → Development → QA, weekly Monday checkpoints; roles PM/PO, UX designer, UX researcher, devs | [UX Improvement Projects](https://project.pages.drupalcode.org/ai/1.4.x/ux/ux_improvement_projects/) |
| Two roles | **Support UX Requests** (triage/answer `Needs UX review`, ~1+/week) and **Join a UX Project Team** ("AI Makers program": researchers, designers, devs, QA) | How to Contribute to UX |

Stated bar: "2+ years of UX and Drupal experience" and ongoing commitment. Treat as a preference, not a gate — the demo story reviews below are being done by people new to the initiative.

### 1.2 Where the design/UX work actually is (open issues, 2026-11-02)

**A. AI demo story reviews — the best first task, no local Drupal needed.** `ai_demo` has 18 open Sprint 21 issues. Each AI feature has a "story" page on the demo site (Northmoor University, 30-day instances from Drupal Forge / new.drupal.org/ai/demo). A UX review = read the story cold, follow it side by side with the demo, record findings on a Figma/Miro/Google Doc board, link the board in a comment. Template: [#3628683 AI Translate story](https://git.drupalcode.org/project/ai_demo/-/issues/3628683) (Goal, Before you start, Task 1 read, Task 2 follow, Task 3 feature-specific). Decision from 26 Oct: "each review pairs with low-fidelity UI exploration so reviews produce solutions, not only problems." Open now: Translate (3628683, claimed), image validation (3628684, claimed), alt text (3628681, unclaimed, unlabelled), first-impression test with a non-Drupal person (3628676), Ask AI UI changes from the story review (3628686), `[META] General UX improvements to the AI Demo` (3628631). Observability, MCP and Content Review stories are queued next.

**B. `Needs UX review` requests (11 open group-wide, 3 on the current sprint).** Design-decision items, not pixel work: how a provider should notify users of better models ([ai#3575689](https://git.drupalcode.org/project/ai/-/issues/3575689)), ai_ckeditor UX with no provider installed (ai#3586549), per-provider timeout setting (ai#3574472), "Improve AI Agents Explorer drastically" (ai#3556394), ai_dashboard compactness (3567899), `[META] Chatbot UX evolution ideas` ([ai_initiative#3544476](https://git.drupalcode.org/project/ai_initiative/-/issues/3544476)).

**C. ai_context (CCC) `what::ux` + accessibility.** 38 open `what::ux` group-wide, 9 in the initiative, 7 on Sprint 21. Mix of wording/label fixes (3586605), listing filters and reset buttons (3586585/3586586), icon bug (3586587), and real design calls: WCAG 3.2.2 "choose a fix" ([3586607](https://git.drupalcode.org/project/ai_context/-/issues/3586607)), `[Meta] CCC accessibility testing` (3586433, postponed), and the **People stream META** ([3586623](https://git.drupalcode.org/project/ai_context/-/issues/3586623), tagged `needs ux review`): "help site builders see which context applies where and why" — a discovery/IA problem waiting for a researcher.

**D. UX-track housekeeping that is pure novice-UX work.** `Review all AI UX meeting notes for future items and create issues` (ai_initiative#3559136), `Revisit AI UX documentation post-Chicago` (3566916), `Create documentation on how to create issues that are testable on DrupalForge` (3583362). Also: the contribute page's non-code list omits UX entirely, and drupal.org's UX contributor-role pages 404 after the migration — both are docs contributions a designer can own.

**E. Adjacent, heavier.** Canvas AI chat UI (project/canvas, 6 sprint issues; designs in canvas#3575780), AI Agents Explorer, chatbot. Real product design, but the Canvas team has its own designers — route via `#ai-ux`, do not cold-pick.

### 1.3 Signal quality and label drift (what the radar has to cope with)

| Label | Group open | In initiative | Sprint 21 |
|---|---|---|---|
| `Needs UX review` | 11 | 3 | 3 |
| `needs ux review` | 8 | 1 | 0 |
| `what::ux` (ai_context) | 38 | 9 | 7 |
| `ux` / `UX` | 13 / 79 | 2 / 0 | 0 |
| `ui` (ai_demo) | — | 1 | 1 |
| `accessibility` / `Accessibility` | 12 / 194 | 2 / 0 | 3 / 0 |
| `Needs design` / `design` | 38 / 52 | 0 | 0 |

Title keyword hits across open `AI Initiative Sprint` issues: accessibility 77, design 28, UX 23, user experience 17, usability 13, demo 19, story 5. So: labels alone miss most of it; the radar must OR over label variants, add a keyword pass, and read `ai_demo` + the current UX meeting issue directly. `Needs usability review` is the drupal-core tag (318 open), not used here — the guide must say which tag to use.

### 1.4 Friction a designer hits on day one

- drupal.org issue links 302→404 mid-migration; GitLab bounces `/-/issues/` to `/-/work_items/`. Always link git.drupalcode.org.
- The drupal.org initiative project page is marked unsupported; the live docs are at project.pages.drupalcode.org and new.drupal.org/ai.
- Meeting time/timezone is not public (Slack only). Demo build repos are partner-only; findings go through the public `ai_demo` queue.
- [AI-use policy](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/policy-on-the-use-of-ai-when-contributing-to-drupal): disclose significant AI-written text; posting unreviewed AI output is an etiquette violation. ai_demo issues carry a three-checkbox disclosure block (verified / reviewed / AI-generated) — the guide adopts it.
- Drupalisms everywhere (node, entity, recipe, CCC, MR, rtbc, needsWork, DrupalForge, Starforge).

## 2. Deliverables

### 2.1 Repo layout (`drupal-ai-ux-contrib`)

```
README.md                      what this is, 5-minute start, which client you use
guide/                         onboarding guide (one page per section, see 2.2)
skills/ai-ux-radar/SKILL.md    canonical skill (Agent Skills spec: name == dir, frontmatter name/description only)
skills/ai-ux-radar/reference/queries.md     API cookbook (anonymous curl, no glab)
skills/ai-ux-radar/reference/lanes.md       lane definitions + scoring
skills/ai-ux-radar/reference/profile.md     team profile template (skills, availability, tools)
scripts/ux_radar.py            zero-dependency fetcher (python3 stdlib) → TSV; the skill calls it when present, falls back to curl
.github/prompts/ai-ux-radar.prompt.md       Copilot adapter (thin pointer, same pattern as drupal-ai-dev)
scripts/install.sh             --client claude|copilot|codex|all : symlink/copy skills/ into .claude/skills, .github/skills, .agents/skills
templates/                     story-review board outline, Needs-UX-review response, UX issue body (with disclosure block), intro message for #ai-ux
```

Portability rule: the skill must run with **no local Drupal, no DDEV, no glab, no composer**. Anonymous `curl` against `https://git.drupalcode.org/api/v4` is enough (all issue endpoints are public; labels endpoints are not, so never depend on them). Fallback mode: paste `SKILL.md` into any chat client with web access and it still works, because every query is a literal URL.

### 2.2 Onboarding guide — sections

1. **Where designers fit in** — the three lanes (Inside AI / Outside AI / People), the UX track, what designers have shipped (Rotterdam demo, story reviews).
2. **First week checklist** — drupal.org account → GitLab sign-in, Slack `#ai-ux` + `#ai` + `#ai-contrib`, intro message (template), start a Drupal Forge demo instance, read the 5 UX docs pages, attend one Monday meeting (read the current meeting issue first).
3. **Where the work is** — the §1.2 map, kept current by running the radar. Which labels mean what; which tag to use (`Needs UX review`, not the core one).
4. **How to do a story review** — the ai_demo protocol step by step, board setup, how to post, what "pair with low-fi exploration" means in practice.
5. **How to answer a `Needs UX review` request** — read the issue against Core UX Principles + hierarchy, propose, sketch, when to escalate to the Monday meeting. Response template.
6. **How to file a UX issue** — required details (version, path, screenshots, expected), labels, parent META, disclosure block, link hygiene.
7. **Etiquette and policy** — AI disclosure, "don't post unreviewed AI text", unanswered `needsWork` reads as abandonment, credit attribution.
8. **Glossary** — Drupalisms and initiative jargon.
9. **FAQ / known breakage** — 404 links, work_items URLs, meeting time via Slack, partner-only repos.

Target ≤ 1,500 words total excluding templates; link to the canonical docs instead of restating them.

### 2.3 `ai-ux-radar` skill — procedure

Read-only. Inputs: optional `reference/profile.md`. Output: ranked chat report; optional `UX-RADAR-<date>.md` if the user asks.

1. **Orient** — read profile (or run generic). Detect current sprint with `x-total` probes on `2026SprintNN` (reuse the drupal-ai-dev §1 method, baseline from a `sprint:` line in profile.md or the user).
2. **Scan** (≤ 8 HTTP calls, all group scope `groups/project`, anonymous):
   - labels `Needs UX review`, `needs ux review`, `what::ux`, `ux`, `ui`, `accessibility` — open, any project (UX requests are instance-wide by design)
   - current-sprint issues with title keywords: UX, usability, accessibility, design, label, wording, icon, dialog, story, demo
   - `ai_demo` open issues (whole project; it is small)
   - the UX meeting issue for the coming Monday (`ai_initiative`, title `Drupal AI UX meeting <date>`) and the previous one: agenda, "Next story reviews", "Next Steps" owners
   - `ai_initiative` open items with `ux` or `Needs UX review`
3. **Classify into lanes**: Review request · Story/usability review · Design exploration (lo-fi, "choose a fix") · Content & naming (labels, help text, principles) · Accessibility audit · IA/menu placement · Research (first-impression tests, discovery METAs) · Housekeeping (notes → issues, docs). Exclude `state::fixed|closed|postponed|blocked|inProgress` and anything assigned, except to show "claimed — watch".
4. **Score /10, arithmetic shown**: fit 0–4 from profile skills · access 0–3 (reproducible on a Forge demo instance = 3; needs screenshots in the issue = 2; needs a local Drupal = 0) · urgency 0–2 (`Needs UX review` older than 3 business days with no response = 2; current sprint label = 1) · effort 0–1 (bounded).
5. **Report**: UX meeting this Monday (what's on, who owes what) → Review requests → Story reviews → Design/discussion → Housekeeping → Watch (claimed). Every link git.drupalcode.org. End with "how to claim" (comment + assign yourself + ETD) and "where to post" per lane.

Explicitly dropped from the developer radar: expertise ledgers, TODO file ownership, MR/pipeline joins, verifiability via PHPUnit, rollover/retro, glab. Keep the budget discipline (one command per scan, no per-issue calls).

### 2.4 Cross-platform mechanics

- Canonical `skills/<name>/SKILL.md` per the Agent Skills spec; `install.sh` places it for Claude Code (`.claude/skills`), Copilot (`.github/skills`), and spec-following clients (`.agents/skills`). Copilot prompt adapter in `.github/prompts/`.
- `scripts/ux_radar.py` is optional sugar: the skill works with curl alone, so chat-only clients (claude.ai, Copilot Chat, ChatGPT with browsing) can run it from the pasted SKILL.md.
- Validate on three clients before release: Claude Code, VS Code Copilot agent mode, one chat client by paste.

## 3. Other skills and items to consider

Skills (in rough value order):

1. **`ai-ux-story-review`** — generate the review protocol from a story URL (tasks/questions in the #3628683 shape), then turn a findings board into the ai_demo "one row per finding + slide link" issue format with the disclosure block. Highest reuse: every demo story gets reviewed.
2. **`ai-ux-review-response`** — structured answer to a `Needs UX review` issue: checks against Core UX Principles and the AI hierarchy, drafts the comment, flags when it belongs in the Monday meeting instead.
3. **`ai-ux-meeting-prep`** — digest the coming Monday's issue + last notes into "what's on / my open actions"; companion mode drafts minutes in the established section format (Overview, Decisions, Questions, Next Steps).
4. **`ai-naming-check`** — audit a module's admin labels and menu placement against the principles and `ai.admin_config_*` parents. Needs a checkout or screenshots; later.
5. **Accessibility** — do not build; reuse the community `drupal-accessibility` skill shipped by `ai_best_practices` and link it from the guide.

Non-skill items:

- **Glossary + link-hygiene page** (fast, high leverage).
- **Weekly digest automation** — GitHub Action runs `ux_radar.py`, commits `UX-RADAR-<date>.md`, optionally posts to a team channel. Lets non-CLI people read the radar without running anything.
- **Upstream docs contributions** the team can own on day one: add UX to the contribute page's non-code list; the meeting-notes-to-issues task (3559136); DrupalForge-testable-issue docs (3583362).
- **Label consolidation proposal** to the UX track (`UX`/`ux`/`what::ux`/`Needs UX review`/`needs ux review`): a tidy win that also simplifies the radar.
- **Figma board index** — one page listing the shared board and per-review decks (the 26 Oct notes link one; others are scattered in issue comments).
- **Pairing**: first review done alongside an existing attendee; ask in `#ai-ux`.

## 4. Phases

| Phase | Scope | Est. |
|---|---|---|
| 0 | Create repo, README, `install.sh`, `profile.md` template, decide name/license | done 2026-11-02 (license open) |
| 1 | Guide sections 2, 3, 4, 6, 8, 9 + templates (the parts a designer needs before the first meeting) | done 2026-11-02 (all 9 sections) |
| 2 | `ai-ux-radar` SKILL.md + queries.md + lanes.md; `ux_radar.py`; Copilot adapter; validate on 3 clients against live API | done 2026-11-02; fetcher validated live, client run-through pending |
| 3 | `ai-ux-story-review` skill (plan + report modes, `story_steps.py`), guide trim | done 2026-11-02 |
| 3b | Zero-config rewrite: script prints the report, self-contained skills, lite scan; profile/lanes/queries/report-formats removed | done 2026-11-02 |
| 4 | Meeting-prep skill; upstream docs issues filed; confirm the lite scan in a web client | next |

Validation per phase: a designer on the team runs the first-week checklist and the radar cold, without help; fix what they trip on before adding more. Re-run the §1.3 label census monthly — the queries in the radar must track drift.

## 5. Decisions needed

1. Repo host and name (GitHub vs git.drupalcode.org; proposed `drupal-ai-ux-contrib`), license.
2. Does the radar write a file by default or chat-only? (Proposed: chat-only, `--write` on request.)
3. Team profile: who, which skills (research / interaction / visual / content design / a11y), weekly hours, Figma access.
4. Whether to offer the skill upstream to `ai_best_practices` once stable (it would then sync into every `.agents/skills/`).
5. Whether to seed the guide with the Monday meeting time once someone gets it from `#ai-ux` (keep it out of the public repo if the track prefers Slack-only).
