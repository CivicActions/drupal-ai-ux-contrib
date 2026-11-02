# 9. FAQ and known breakage

**The drupal.org link in an issue 404s.** The platform is mid-migration. Rebuild the link as `https://git.drupalcode.org/project/<name>/-/issues/<iid>` with the same number. GitLab may redirect to `/-/work_items/<iid>`; same page.

**The drupal.org "AI Initiative" project page says unsupported.** It is legacy. Current entry points: https://new.drupal.org/ai and the module docs at https://project.pages.drupalcode.org/ai/1.4.x/.

**When is the UX meeting?** Mondays, weekly. Time and link are shared in `#ai-ux` only. The agenda and notes are public in the `ai_initiative` meeting issue.

**I cannot find the demo source code.** The build repositories are partner-only. Everyone can file and comment in the public `ai_demo` queue; partners triage and build.

**Do I need a local Drupal?** No for story reviews, request answers, content and accessibility findings on the demo. Yes to review a merge request's UI before it merges; ask a developer to pull it up, or the author for screenshots.

**Which UX tag?** `Needs UX review` in the AI ecosystem. `Needs usability review` is Drupal core's tag and the core UX team's queue.

**Someone is already assigned.** Leave it unless the issue has been silent for two weeks; then ask on the issue whether help is wanted.

**The radar shows something labelled `state::fixed` but still open.** Labels lag. Treat `fixed`, `closed`, `postponed` as done.
