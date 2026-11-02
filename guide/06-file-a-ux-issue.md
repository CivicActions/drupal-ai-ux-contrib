# 6. How to file a UX issue

Issues are created on git.drupalcode.org in the project's queue (`New issue`; GitLab may call them work items). Use the project's issue templates when offered; `ai_demo` has Bug report, Feature request, Feature page, Support request, Task and Plan.

Body: [templates/ux-issue.md](../templates/ux-issue.md). Always include:

- Module and version (or "AI demo, instance started <date>"), and the URL path, for example `/admin/config/ai/settings`.
- Screenshots or a short video. Crop and annotate.
- What happens, what you expected, who it affects (editor, site builder, visitor).
- Your proposal, even rough. Link the slide or board frame.
- The AI disclosure block (three checkboxes; see [07-etiquette-and-policy.md](07-etiquette-and-policy.md)).

Labels: pick the type (`category::bug|feature|task|plan`); add `Needs UX review` only when you are asking the UX track for a decision, not when you are the UX track reporting a finding. Leave sprint and `state::` labels to the maintainers unless told otherwise. Link the parent META in the first line (`Parent: #3628631`) when one exists.

One finding per issue. A review that found eight things is eight issues plus one summary comment on the review issue, not one issue with eight bullets.

Links: always `https://git.drupalcode.org/project/<name>/-/issues/<iid>`. drupal.org issue URLs 404.
