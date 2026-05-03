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
- **Sonnet stall -> Opus retry**: Daily-briefing dispatch occasionally stalls on Sonnet mid-stream (watchdog timeout, usually during email/calendar fan-out). Recovery pattern: retry the same dispatch with model="opus" override. Confirmed working 2026-04-14 (original Poseidon/Eos fix) and again 2026-04-23. If first Sonnet run stalls, go straight to Opus on retry rather than re-attempting Sonnet.
- **Second Gmail access ownership**: The built-in Gmail connector currently profiles as `edgar.agunias@gmail.com`. Any second Gmail account access for dispatches should use a local terminal OAuth/token path stored outside the repo, suggested location `~/.config/claudia/gmail-second/`. Eos is the operational owner because dispatches will use the account most often; Hephaestus should be the implementation helper if scripts, token probes, or CLI wrappers are needed. Do not attempt OAuth login or request credentials inside an agent handoff.
- **Second Gmail OAuth active**: As of 2026-05-01, the terminal OAuth path for the second Gmail account is active at `~/.config/claudia/gmail-second/gcloud/application_default_credentials.json`. Read-only Gmail API testing confirmed the account as `eagunias@ucsd.edu` with recent message metadata available via local scripts. Use this path for UCSD inbox checks when the built-in Gmail connector remains tied to `edgar.agunias@gmail.com`.
