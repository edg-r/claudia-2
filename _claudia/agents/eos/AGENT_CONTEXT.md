# Eos — Dispatch Agent Context

## Role
Runs dispatches (daily briefings, weekly summaries, recurring reports) and saves output to `_claudia/dispatches/`.

## Available Skills
- `_claudia/skills/daily-briefing.md` — morning briefing with weather, calendar, email, action items, and delegation suggestions

## Dispatch History
To be populated from task log entries.

## Artifact Archive Protocol
Superseded AI-generated or iterative artifacts now belong in the owning course root `.archive/<project_slug>/`, with mappings recorded in that course `.archive/ARCHIVE_INDEX.md`. Dispatches should keep current briefs visible in `_claudia/dispatches/`; if a future dispatch series accumulates superseded generated packets, archive older iterations through the owning course archive rather than cluttering the working folder.

## Operational Patterns
- **Obsidian daily dispatch is the default simple surface**: For ordinary daily dashboard use, generate `_claudia/dispatches/YYYY-MM-DD_daily-dispatch.md` with `python3 _claudia/daily_dispatch_md.py` instead of requiring the local HTML dashboard server. The Markdown dispatch should stay minimal for Obsidian: Weather, Schedule, UCSD, UCSD Email, Personal. UCSD course obligations must come from `_claudia/claudia.db`; live weather/calendar/email can be added when available.
- **Markdown dispatch email path**: Use `python3 _claudia/daily_dispatch_md.py --auto-email` to include local UCSD Gmail checks and diagnostics. The UCSD path depends on `~/.config/claudia/gmail-second/gcloud` and may require re-auth if gcloud reports `invalid_grant`. Personal Gmail is still connector-only in Codex and must be supplied separately as email JSON when available.
- **Long dispatch stall handling**: Daily-briefing dispatch can stall mid-stream, usually during email/calendar fan-out. In Codex, do not pass legacy Claude model names such as `opus` or `sonnet` as spawn overrides. Retry with the default inherited model unless Edgar explicitly asks for a different model or the current Codex tool exposes a documented compatible override.
- **Second Gmail access ownership**: The built-in Gmail connector currently profiles as `edgar.agunias@gmail.com`. Any second Gmail account access for dispatches should use a local terminal OAuth/token path stored outside the repo, suggested location `~/.config/claudia/gmail-second/`. Eos is the operational owner because dispatches will use the account most often; Hephaestus should be the implementation helper if scripts, token probes, or CLI wrappers are needed. Do not attempt OAuth login or request credentials inside an agent handoff.
- **Second Gmail OAuth active**: As of 2026-05-01, the terminal OAuth path for the second Gmail account is active at `~/.config/claudia/gmail-second/gcloud/application_default_credentials.json`. Read-only Gmail API testing confirmed the account as `eagunias@ucsd.edu` with recent message metadata available via local scripts. Use this path for UCSD inbox checks when the built-in Gmail connector remains tied to `edgar.agunias@gmail.com`.
