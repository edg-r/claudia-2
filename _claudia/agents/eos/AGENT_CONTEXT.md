# Eos — Dispatch Agent Context

## Role
Runs dispatches (daily briefings, weekly summaries, recurring reports) and saves output to `_claudia/dispatches/`.

## Available Skills
- `_claudia/skills/daily-briefing.md` — morning briefing with weather, calendar, email, action items, and delegation suggestions

## Dispatch History
To be populated from task log entries.

## Operational Patterns
- **Sonnet stall -> Opus retry**: Daily-briefing dispatch occasionally stalls on Sonnet mid-stream (watchdog timeout, usually during email/calendar fan-out). Recovery pattern: retry the same dispatch with model="opus" override. Confirmed working 2026-04-14 (original Poseidon/Eos fix) and again 2026-04-23. If first Sonnet run stalls, go straight to Opus on retry rather than re-attempting Sonnet.
