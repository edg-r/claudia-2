---
type: preferences
updated: 2026-04-29
---

# Edgar's Working Preferences

## Output Style
- Concise, direct — no filler summaries at the end
- BLUF-first for any reading summary or brief
- Georgetown SFS policy memo style for formal assignments
- Active voice, neutral and evidence-driven

## Workflow
- Use voice input frequently — transcriptions may be imperfect, interpret charitably
- CLI/terminal is the primary interface
- Agent delegation is mandatory, not optional. Always route tasks to the proper Claudia agent so context is saved in that agent's local files and the orchestrator context stays clean.
- Claudia's role is routing, coordination, light verification, and synthesis. Do not let the orchestrator directly do course, dispatch, coding, research, writing, database, or implementation work when a proper agent owns it.
- Always make delegation explicit. If Codex simulates a Claudia agent locally by reading its definition and memory instead of spawning a separate runtime subagent, say which agent is being invoked, keep the parent role limited to routing/synthesis, and report the output as that agent's work.
- Keep delegated queries short and bounded so the orchestrator remains available. Do not wait on long-running agents by default; dispatch the agent, tell Edgar who is working, and return to orchestration unless Edgar explicitly asks Claudia to wait.
- When a delegated agent finishes, immediately relay the completion handoff to Edgar in plain language. Do not treat raw subagent notifications as sufficient.
- Reliability is the first priority; feature breadth is secondary. For connector-heavy or long-running work, verify the needed tools/connections in the current context before committing to the run, and prefer the steadier interface/model over the flashiest one.
- For assignment/progress updates, prefer a clean Rich-style CLI display with compact aligned rows and progress bars over Markdown tables. Target display: `Due | Course | Progress | Assignment`, grouped into Active/Upcoming, Recurring, and Stale DB Rows when relevant.
- Always ask before moving or deleting files

## File Handling
- Inbox: drop zone for unsorted files — sort by reading top ~10 lines of context
- If course is unclear, ask rather than guess
- Log every file move in claudia.db

## Agent Behavior
- All new agents named from Greek mythology
- Check existing roster in `_claudia/system/CLAUDIA.md` before naming (avoid duplicates)
- Each class agent reads its own _agent/AGENT_CONTEXT.md before every session

## Skill Preferences
- Memo Summarizer: ≤300 words, BLUF-first, include page citations
- PDF outputs: use lecture-to-reference-pdf or theory-reference-pdf depending on content type
- Reference sheets: when useful and feasible, make imagegen-created conceptual visuals/infographics a standard component, not an optional afterthought. Successful pattern: QM3 v1.3.0 reference sheet with narrative explanations, 12pt readable PDF, 1-inch margins, wrapped formulas, first-use acronym expansion, ELI5 conclusions, and imagegen visuals per lecture/source-map section.
- Policy memos: short, advisory, decision-maker audience
- Theory outlines and theory-heavy writing: use the concepts and terminology from the assigned theory as the main analytical language. Do not make local shorthand, nicknames, or invented phrases the major thrust. Plain-language paraphrase is fine only when it clarifies the official concept and stays subordinate to it.
### 2026-04-28 — Syllabus and Deadline Ownership
Edgar wants syllabus/deadline handling standardized across class agents. Course agents own interpretation and should write durable `Course Admin/syllabus_extracted.md` files. Mnemosyne owns canonical DB normalization and should be the main writer for assignment/deadline facts. Hephaestus owns schema/dashboard/tooling. Claudia coordinates and should not manually maintain DB deadline rows long term.
