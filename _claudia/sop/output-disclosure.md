---
name: output-disclosure
description: All agent outputs must include a disclosure block with model, date, sources, and attribution
applies_to: all agents
---

# Output Disclosure

Every agent output — briefings, summaries, analyses, memos, draft assignments — must end with a disclosure block. This ensures transparency about how the content was generated.

## Format

```
---
Generated for: Edgar Agunias
Date: [YYYY-MM-DD]
Model: [model name and version, e.g. Claude Opus 4.6]
Sources: [brief summary of inputs used — e.g. "UCSD email, Google Calendar, web search for La Jolla weather" or "Krugman Ch. 4, lecture slides Week 3"]
Agent: [agent name, e.g. Eos, Plutus, Atlas]
---
```

## Rules

- Place the disclosure at the very end of the output, after all content.
- The sources line should be specific enough that a reader understands what data informed the output, but does not need to be exhaustive. A short summary is fine.
- If multiple agents contributed, list all of them.
- If Claudia (the orchestrator) synthesized outputs from multiple agents, Claudia should be listed as the primary agent with contributors noted.
