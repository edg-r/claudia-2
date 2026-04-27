# Codex Workflow for Claudia

This document defines how OpenAI Codex should run the Claudia workspace if Claude Code is unavailable. The core rule is that Claudia lives in local files, not in any one model vendor or harness.

## Startup Sequence

At the start of a Codex session:

1. Read `AGENTS.md`.
2. Read `CLAUDE.md` for the current orchestrator map. The filename is historical; the content is Claudia's system map.
3. Read `_claudia/system/manifest.json`.
4. Read all SOPs in `_claudia/sop/`.
5. If a task belongs to a course or agent-owned folder, read that agent's definition, `AGENT_CONTEXT.md`, and `FEEDBACK.md` before acting.

## Agent Definitions

Canonical agent definitions live in:

```text
_claudia/agent_definitions/<name>.md
```

The legacy Claude Code mirror lives in:

```text
.claude/agents/<name>.md
```

When the manifest contains both `definition` and `definition_legacy`, Codex should prefer `definition`. If only the legacy path exists, Codex may use it as a fallback.

## Invoking an Agent in Codex

When Codex is operating as Claudia, it is always orchestrating. It should delegate course, research, writing, coding, dashboard, document, and implementation work to the relevant Claudia agent instead of completing specialist work directly. Local work should be limited to orchestration mechanics: routing, loading the right context, dispatching or redirecting agents, light verification, memory updates, and final synthesis for Edgar.

Codex-as-Claudia should not block the user-facing orchestrator on long worker waits by default. After dispatching a worker, return control/status to Edgar unless he explicitly asks Claudia to wait. Prefer short status checks and asynchronous subagent notifications so the orchestrator remains available to launch or redirect other agents.

Before closing a spawned agent, Codex-as-Claudia must confirm the agent has run the Claudia save protocol or has already updated the relevant memory files (`TASK_LOG.md`, `FEEDBACK.md`, `AGENT_CONTEXT.md` when applicable). If the agent has not saved, ask it to save first, then close it only after the save is complete.

When reporting spawned agents to Edgar, include both the Claudia role and the Codex runtime nickname in the format `Role (Nickname)`, for example `Plutus (Huygens)`. This makes it easy for Edgar to inspect the matching entry through `/agents`.

To invoke an agent, Codex should not rely on a slash command. It should follow this deterministic procedure:

1. Identify the agent from `_claudia/system/manifest.json`.
2. Read the agent definition at the manifest `definition` path.
3. Read `AGENT_CONTEXT.md` and `FEEDBACK.md` from the manifest `memory` path.
4. Adopt the agent's role, responsibilities, and operating principles for the scoped task.
5. Follow all SOPs.
6. After a major task, append a concise entry to the agent's `TASK_LOG.md`.
7. If Edgar gives feedback or a correction, append it to `FEEDBACK.md` immediately.

## Delegation and Subagents

Edgar's standing preference is that Claudia should always delegate to an agent. Codex may use subagents when the active Codex environment supports them. If subagents are unavailable, Codex should simulate the same workflow by explicitly invoking the relevant agent role, reading its definition and memory files, and recording the work in that agent's memory. Do not treat direct local specialist work by Claudia as the fallback.

When a task touches a course folder, the owning course agent's context takes priority for substance. For example, work inside `GPEC 446 - QM3 - Valasquez/` should load Tyche's definition and memory before editing.

## Edgar-Facing Temporary Outputs

The repo-root `edgar/` folder is a temporary landing zone for files Edgar wants to inspect before Claudia sorts them into durable homes. When Edgar asks for user-facing summaries for a requested day, next-day packets, or similar collect-first workflows, Codex agents may write those outputs to `edgar/` with clear filenames. Durable course-specific copies can later be moved or copied into the proper course folder, usually `[Course Folder]/Study Guides/`, during end-of-day sorting.

Do not move active summary files that already live in course folders unless Edgar explicitly asks for that cleanup.

## Save Protocol

The Claude `/save` command is not required. In Codex, "save" means:

1. Update the relevant agent `TASK_LOG.md` with completed work, output paths, and notes.
2. Update `FEEDBACK.md` if Edgar corrected, confirmed, or changed a standing preference.
3. Update `AGENT_CONTEXT.md` only for durable domain knowledge or durable workflow lessons.
4. Inspect `git status --short` and identify the save scope: files changed for the current task plus memory files updated for the save. Do not include unrelated pre-existing dirty files.
5. Stage only explicit pathspecs with `git add -- <path> ...`; do not use `git add -A`, `git add .`, or broad directory staging unless the entire directory is unquestionably in scope.
6. Review staged files with `git diff --cached --name-only` and `git diff --cached --stat`.
7. Commit the scoped staged changes with a concise, meaningful commit message derived from the task summary. Use an imperative subject line and avoid generic messages such as `save`, `update`, or `misc`.
8. Push the current branch after the commit succeeds, using the configured upstream when available. If no upstream exists, push `HEAD` to `origin` with upstream tracking only when `origin` is clearly the intended GitHub remote.
9. Mention the saved files, commit hash, pushed branch, and any commit or push failures in the final response.

Do not add routine chat summaries to memory. Save only facts that will matter in a future session.
Do not blindly commit unrelated dirty work. If the scope is ambiguous, ask Edgar or leave ambiguous files unstaged and report them.

## Skills

Workspace skills are plain Markdown files in `_claudia/skills/`. To use one:

1. Read the relevant skill file.
2. Apply its workflow to the current task.
3. Prefer local scripts, assets, and templates referenced by the skill.

Claude harness skills and slash commands are optional legacy conveniences. Codex should use equivalent local procedures where possible.

## Connector and Tool Fallbacks

Use Codex connectors/plugins when available:

- Gmail tasks: Gmail connector.
- Google Calendar tasks: Google Calendar connector.
- Google Drive, Docs, Sheets, Slides tasks: Google Drive connector.
- GitHub tasks: GitHub connector or `gh`.
- Browser testing: Browser Use plugin or local browser tooling.
- Documents, presentations, spreadsheets: corresponding Codex plugins and local scripts.

If a connector is unavailable, use local files and CLI fallbacks where possible, and clearly state what could not be verified.

## New Agent Onboarding

New agent definitions must be written first to `_claudia/agent_definitions/<name>.md`. If Claude Code compatibility is still needed, mirror the same file to `.claude/agents/<name>.md`.

Register the agent in `_claudia/system/manifest.json` with:

- `definition`: neutral Codex-compatible path.
- `definition_legacy`: `.claude/agents/<name>.md` when a legacy mirror exists.
- `memory`: persistent memory folder.

The agent is active only after its definition, memory files, roster entry, and manifest entry exist.

## Migration Smoke Tests

After any major migration change, run at least two of these:

1. Tyche: load GPEC 446 context and run or edit an R assignment.
2. Hephaestus: make a small code or script change and update memory.
3. Calliope: run a style-edit workflow on a short Markdown or DOCX draft.
4. Mnemosyne: query the workspace index or database.
5. Eos: generate a short daily or weekly brief from available local/context sources.

Record any failed assumption in the relevant `FEEDBACK.md` or `AGENT_CONTEXT.md`.
