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
### Artifact Archive Protocol

Mnemosyne owns discovery for course-local archives. Superseded AI-generated or iterative artifacts belong in the owning course root `.archive/<project_slug>/`, with mappings recorded in that course `.archive/ARCHIVE_INDEX.md`. Keep source readings, professor-provided files, final submitted files, and the latest active working/clean/submission candidate visible in the course folder. When asked to locate or revert an older draft, search the owning course archive index before scanning the whole repo.
