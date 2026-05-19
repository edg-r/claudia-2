# Hephaestus -- Feedback Log

Corrections and confirmed approaches from Claudia and Edgar.

## 2026-04-23 — Study/coursework blocks go on Learning calendar
Course study, reading, and assignment timeblocks belong on Edgar's Learning calendar (`dicjpk2av0g6nkujknnesgu8fs@group.calendar.google.com`), not the primary calendar. Primary is for non-study events. When creating timeblocks for HW, memos, readings, or study sessions, set `calendarId` to Learning from the start. Google Calendar MCP has no native move, so getting this wrong forces a delete-and-recreate cycle.

## 2026-04-23 — Emdash/en-dash rule applies to calendar event titles
The "no emdashes" style rule extends to calendar event summaries. Google Calendar MCP accepts `—` and `–` verbatim with no filtering. Use ` - ` (space-hyphen-space) or a colon instead. Applies at creation time; catching it post-hoc means a second update pass per event.

## 2026-04-23 — Verify tool context before committing to an MCP-dependent plan
Per-run tool availability for this agent varies. Google Calendar MCP tools were present in one run and absent in the next within the same session. Before promising a plan that depends on a specific MCP (Calendar, Gmail, Drive), confirm the relevant tools are loaded in the current context. If missing, either load via ToolSearch or hand the step back to Claudia rather than silently failing.

## 2026-05-19 — GPSA budget flow is a positive example
**Type:** confirmation
**What:** Edgar confirmed `edgar/gpsa_budget_flow.html` as a positive example for future budget-flow visualizations.
**Why:** The artifact captures the desired interaction and polish: pastel Sankey flow, smooth no-snap year-over-year animation, upstream highlighting, ordered line items, and scrollable reallocation cards.
**Rule going forward:** For budget workbook visualization requests, use `_claudia/skills/budget-flow-visualization.md` and treat `edgar/gpsa_budget_flow.html` as the reference benchmark unless Edgar asks for a different direction.
