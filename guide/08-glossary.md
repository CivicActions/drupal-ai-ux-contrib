# 8. Glossary

| Term | Meaning |
|---|---|
| Node, entity | A piece of content (node = page/article; entity = anything stored: content, user, taxonomy term) |
| Site builder | Person who configures Drupal through the admin UI without code; the primary audience of the UX principles |
| Recipe | An installable bundle of configuration and content; the demo's features are recipes |
| Contrib, module | Community-maintained add-on; `drupal/ai` is the main AI module, `ai_agents`, `ai_ckeditor`, `ai_translate` are others |
| Provider | A module connecting Drupal to an LLM vendor (OpenAI, Anthropic, local models) |
| Agent, tool, function call | An agent is an LLM loop that can call tools; a tool is one callable action |
| CCC, ai_context | Context Control Center: where site builders define the context (instructions, facts) pushed to AI features |
| MCP, Tool API | Protocols that let external agents (Claude Code, Cursor) act on Drupal: the "Outside AI" lane |
| Canvas | Drupal Canvas, the visual page builder (formerly Experience Builder); has its own AI chat |
| Drupal Forge | Hosted trial instances; the AI demo runs there, free for 30 days |
| Starforge / AI Tracker | Dashboard that renders `[Tracker]` metadata from issues; not a separate data source |
| Issue, work item | Same thing; GitLab's new UI calls issues work items |
| MR | Merge request, GitLab's pull request |
| iid | The issue number, e.g. 3628683, stable across the drupal.org → GitLab migration |
| `state::needsReview` / `rtbc` / `needsWork` | Awaiting review / "reviewed and tested by the community", ready to merge / changes requested |
| Sprint | Two-week cycle, label `2026SprintNN` |
| META, [Meta], [Plan] | Umbrella issue holding child issues or a plan |
| Drupalism | Jargon like the above; the UX principles say to keep it out of primary labels |
