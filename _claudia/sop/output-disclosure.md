---
name: output-disclosure
description: Portable agent deliverables must include a disclosure block with model, date, sources, and attribution
applies_to: all agents
---

# Output Disclosure

Every agent **deliverable** — briefings, summaries, analyses, memos, draft assignments, explainers, study guides, dispatches, any file written to disk or report returned as a standalone document — must include a disclosure block. This ensures transparency about how the content was generated, because deliverables travel out of the live session into other contexts (Word, inbox, dispatches folder, future sessions) where model/date/agent provenance matters.

**Live conversational replies are out of scope.** Claudia's end-of-turn messages to Edgar, /save confirmations, routine status updates, and any other chat-stream output do NOT carry the disclosure block. Context is already scoped by the session; an extra footer on every reply adds noise without traceability. Disclosure belongs on outputs that travel, not on outputs that stay inside the conversation.

## Format

```
---
Generated for: Edgar Agunias
Date: [YYYY-MM-DD]
Model: [exact model name/version and reasoning effort when known, e.g. GPT-5.5 (medium reasoning) or Claude Opus 4.6]
Sources: [brief summary of inputs used — e.g. "UCSD email, Google Calendar, web search for La Jolla weather" or "Krugman Ch. 4, lecture slides Week 3"]
Agent: [agent name, e.g. Eos, Plutus, Atlas]
---
```

## Rules

- Place the disclosure at the very end of the output, after all content, unless the deliverable has a designed title page or cover page where provenance is more useful to Edgar.
- For title-page or cover-page deliverables, place the disclosure/provenance block on the title page. This is preferred for daily class packets and other multi-section PDFs where an end footer can get separated from the document context.
- Use the most specific model provenance available. If the session exposes a model name, version, and reasoning effort, include all of them; do not collapse it to a generic family name such as "GPT-5."
- The sources line should be specific enough that a reader understands what data informed the output, but does not need to be exhaustive. A short summary is fine.
- If multiple agents contributed, list all of them.
- If Claudia (the orchestrator) synthesized outputs from multiple agents, Claudia should be listed as the primary agent with contributors noted.
