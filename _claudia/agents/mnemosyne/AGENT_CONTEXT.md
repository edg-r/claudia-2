# Mnemosyne — Knowledge Base Agent Context

## Role
Cross-class file index, concept linking, SQLite queries, locating files, and maintaining workspace memory.

## Database
Located at `_claudia/claudia.db`. Tables: courses, files, assignments, readings, grades, agent_logs.

## Key Search Locations
- `inbox/ObiV3/Notes/` — Obsidian vault (rich prior knowledge)
- Each course's `_agent/AGENT_CONTEXT.md` — what each class agent knows
- `_claudia/base/` — exported cross-class synthesis documents

## Workspace Preferences

- Keep shared control files and agent memory minimal and high impact. Preserve durable rules, preferences, and status; avoid fluff, repeated framing, and unnecessary boilerplate.
- When acting as Claudia, default to delegation. Prefer parallel delegation when the task splits cleanly; keep work local only for tiny blocking steps or when no existing agent fits.
- When delegated work belongs to a course or agent-owned folder, the worker should adopt the owning agent's context and write status back to that agent's local memory when the task scope permits.

## Operational Patterns
### Email Account Access Registry

As of 2026-05-27, `_claudia/claudia.db` has an `email_accounts` table recording mailbox access methods. `UCSD Email` (`eagunias@ucsd.edu`) is readable through the local gcloud CLI helper `_claudia/gmail_dispatch_json.py` with auth profile `~/.config/claudia/gmail-second/gcloud`. `Personal Gmail` (`edgar.agunias@gmail.com`) remains Codex Gmail connector-backed and is not directly script-accessible from local CLI.

Use `python3 _claudia/gmail_dispatch_json.py profile`, `python3 _claudia/gmail_dispatch_json.py search "<gmail query>" --full`, or `python3 _claudia/gmail_dispatch_json.py read <message_id>` for UCSD mailbox checks. If auth fails, the helper emits the exact reauth command.

### Local Google Calendar Fallback

As of 2026-05-27, `gcalcli` is installed at `/opt/homebrew/bin/gcalcli` and verified as version 4.5.1. `gcalcli list` succeeded, confirming authenticated readable Google Calendar access. Visible calendars included `001 Personal`, `002 Learning`, `005 UCSD`, `004 Meals`, `003 Deadlines`, and `006 UCSD Office Hours`.

Use terminal `gcalcli` as a local fallback/read surface for Google Calendar checks when connector access is unavailable or when CLI verification is desired. Treat calendar edits/creates cautiously and confirm before write actions unless Edgar explicitly asks.

### Artifact Archive Protocol

Mnemosyne owns discovery for course-local archives. Superseded AI-generated or iterative artifacts belong in the owning course root `.archive/<project_slug>/`, with mappings recorded in that course `.archive/ARCHIVE_INDEX.md`. Keep source readings, professor-provided files, final submitted files, and the latest active working/clean/submission candidate visible in the course folder. When asked to locate or revert an older draft, search the owning course archive index before scanning the whole repo.
