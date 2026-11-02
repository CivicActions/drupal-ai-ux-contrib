# Query cookbook — git.drupalcode.org API, anonymous

`<API>` = `https://git.drupalcode.org/api/v4` (or the `DRUPALCODE_API` value a project states). Write the URL literally; no variables. Group scope `groups/project` covers every contrib project. Issue endpoints are public; **labels endpoints are not reliable anonymously** — nothing below uses them. URL-encode spaces as `%20` and `::` stays literal. One `curl` per section; read `x-total` / `x-next-page` headers for counts and paging.

`scripts/ux_radar.py` runs all of this in one command. The twins below are for clients without a shell.

## §1 Sprint detection

```bash
# repeat for NN, NN+1, NN+2; group total and project-ai total
curl -sI "<API>/groups/project/issues?state=opened&labels=2026Sprint<NN>&per_page=1" | grep -i x-total:
curl -sI "<API>/projects/project%2Fai/issues?state=opened&labels=2026Sprint<NN>&per_page=1" | grep -i x-total:
```

Current sprint = highest N with ai ≥ 1. Higher N active only elsewhere = pre-tagging, not rollover.

## §2 UX review requests (instance-wide)

```bash
curl -s "<API>/groups/project/issues?state=opened&labels=Needs%20UX%20review&per_page=100" \
  | jq -r '.[] | [.references.full, (.labels|join(",")), ([.assignees[].username]|join(";")), .updated_at[:10], .title, .web_url] | @tsv'
# lower-case variant
curl -s "<API>/groups/project/issues?state=opened&labels=needs%20ux%20review&per_page=100" | jq -r '…same…'
```

## §3 UX-labelled items on initiative projects

```bash
# one per label: what%3A%3Aux  ux  ui  accessibility  Accessibility  Needs%20design
curl -s "<API>/groups/project/issues?state=opened&labels=what%3A%3Aux&per_page=100" | jq -r '…same…'
```

Keep only projects that appear in §4 (initiative projects) plus ai_demo, ai_initiative, ai, ai_context, ai_agents, ai_ckeditor, canvas.

## §4 Current-sprint keyword pass

```bash
curl -s "<API>/groups/project/issues?state=opened&labels=2026Sprint<NN>&per_page=100&page=1" \
  | jq -r '.[] | select(.title|test("UX|usability|accessib|WCAG|design|label|wording|icon|dialog|modal|story|demo|help text|naming|first.impression|user experience";"i")) | [.references.full, (.labels|join(",")), ([.assignees[].username]|join(";")), .updated_at[:10], .title, .web_url] | @tsv'
# page=2 if x-next-page is set; same for labels=AI%20Initiative%20Sprint (3 pages)
```

## §5 The demo queue

```bash
curl -s "<API>/projects/project%2Fai_demo/issues?state=opened&per_page=100" | jq -r '…same…'
```

## §6 UX meeting issues

```bash
curl -s "<API>/projects/project%2Fai_initiative/issues?search=UX%20meeting&in=title&per_page=100&order_by=created_at" \
  | jq -r '.[] | [.iid, .state, .title, .web_url] | @tsv'
# notes are in the description of the most recent past Monday's issue:
curl -s "<API>/projects/project%2Fai_initiative/issues/<iid>" | jq -r '.description'
```

## Label census (run monthly; adjust REQUEST_LABELS / SCOPED_LABELS in the script)

```bash
# for each candidate label: how many open group-wide, how many in the initiative
curl -sI "<API>/groups/project/issues?state=opened&labels=<label>&per_page=1" | grep -i x-total:
curl -sI "<API>/groups/project/issues?state=opened&labels=<label>,AI%20Initiative%20Sprint&per_page=1" | grep -i x-total:
```

2026-11-02 census (group / initiative): `Needs UX review` 11/3 · `needs ux review` 8/1 · `what::ux` 38/9 · `ux` 13/2 · `UX` 79/0 (other projects; not used) · `accessibility` 12/2 · `Accessibility` 194/0 · `Needs design` 38/0 · `design` 52/0 · `Needs usability review` 9/0 (Drupal core's tag).

## Quirks

- Labels live on issues, not MRs.
- `state::*` labels lag the real state; open issues carry `fixed`/`closed`.
- drupal.org issue URLs 404; emit `https://git.drupalcode.org/project/<name>/-/issues/<iid>`. `web_url` from the API may say `/-/work_items/`; same page.
- 429 → honor `Retry-After` once, then proceed with partial data and flag it.
