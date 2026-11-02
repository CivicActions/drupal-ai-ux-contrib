# 5. How to answer a `Needs UX review` request

The track promises acknowledgement within three business days, simple answers within a week, and escalation of complex ones to the Monday meeting. You can be the person who delivers that.

1. **Acknowledge** within the window, even if only "looking at this, answer by Thursday".
2. **Check the request is complete**: module and version, URL path, screenshots, the problem and expected behaviour. If not, ask for the missing part and stop; that is a valid first response.
3. **Reproduce** on a demo instance where possible. If it needs a local site or a specific module, say what you reviewed from (screenshots, the issue text) and that you did not run it.
4. **Review against the standards**: [Core UX Principles](https://project.pages.drupalcode.org/ai/1.4.x/ux/core_ux_principles/) (naming order: accurate → site-builder friendly, no Drupalisms → developer context in descriptions → benefit language; progressive disclosure; hierarchy over flat lists) and [the AI menu hierarchy](https://project.pages.drupalcode.org/ai/1.4.x/ux/organizing_ai_modules_and_features/) (Infrastructure → Tools & Automation → Features). Add a quick accessibility pass: keyboard, focus, contrast, context changes on input.
5. **Propose, do not only critique.** A sketch, a before/after label table, or a one-paragraph recommendation. Use [templates/ux-review-response.md](../templates/ux-review-response.md).
6. **Decide the route.** Clear answer → post it and remove the `Needs UX review` label if you can (or ask the maintainer to). Trade-off between options or a cross-module pattern → post your analysis and say "bringing this to Monday's UX meeting", then add it to that week's meeting issue.
7. **Follow up.** If the maintainer replies with questions, answer. Silence after a question is read as abandonment.
