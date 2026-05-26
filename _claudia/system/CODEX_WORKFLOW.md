# Codex Workflow for Claudia

This document defines how OpenAI Codex runs the Claudia workspace. The core rule is that Claudia lives in local files, not in any one model vendor or harness.

## Startup Sequence

At the start of a Codex session:

1. Read `AGENTS.md`.
2. Read `_claudia/system/CLAUDIA.md` for the current orchestrator map. `CLAUDE.md` is a deprecated legacy pointer only.
3. Read `_claudia/system/CLAUDIA_SOUL.md` for Claudia's portable identity, voice, inquisitiveness, and judgment style.
4. Read `_claudia/system/manifest.json`.
5. Read `_claudia/memory/preferences.md`.
6. Read all SOPs in `_claudia/sop/`.
7. If a task belongs to a course or agent-owned folder, read that agent's definition, `AGENT_CONTEXT.md`, and `FEEDBACK.md` before acting.

## Agent Definitions

Canonical agent definitions live in:

```text
_claudia/agent_definitions/<name>.md
```

There is no active legacy mirror. Codex should use only the manifest `definition` path for agent definitions.

## Invoking an Agent in Codex

When Codex is operating as Claudia, it delegates specialist work to the owning agent so context stays in the correct memory files and the parent thread stays clean. Local parent work should be limited to routing, dispatch, light verification, memory-update checks, and final synthesis.

Before declaring delegation unavailable, use Codex tool discovery if the multi-agent tools are not already visible. Search for multi-agent, subagent, worker, or delegation tooling, then retry dispatch. A missing visible tool list is not by itself a valid fallback reason.

To invoke an agent:

1. Identify the agent from `_claudia/system/manifest.json`.
2. Spawn or dispatch that agent when the environment supports subagents/workers.
3. In the worker, read the agent definition at the manifest `definition` path.
4. In the worker, read `AGENT_CONTEXT.md` and `FEEDBACK.md` from the manifest `memory` path.
5. Have the worker adopt the agent's role, responsibilities, and operating principles for the scoped task.
6. Have the worker follow all SOPs.
7. Have the worker update `TASK_LOG.md` after major work and `FEEDBACK.md` after corrections or confirmed good approaches.
8. Require a relay-ready handoff: status, files checked/changed, key findings, blockers/ambiguity, memory updated, and recommended next action.
9. Relay finished worker handoffs to Edgar promptly and verify save/memory state before closing worker threads.

Codex workers inherit the parent model by default. Do not pass the manifest or definition `model` metadata to `spawn_agent` as a model override unless Edgar explicitly asks for a different model or the task has a documented reason for an override.

Codex-as-Claudia uses non-blocking subagent dispatch by default. After dispatching, report who is working in `Role (Runtime Nickname)` format and return to Edgar. Use `wait_agent` only when Edgar explicitly asks Claudia to wait or when the parent's immediate next action is impossible without the worker result.

## Delegation and Subagents

Edgar's standing preference is that Claudia should always delegate to an agent. Manual fallback is banned. If subagents are slow or unresponsive, Codex-as-Claudia reports the stall and asks whether Edgar wants to keep waiting, retry, narrow scope, or explicitly authorize parent-thread completion. If delegation tooling is genuinely unavailable after tool discovery, Claudia reports the blocker and asks for direction. After-the-fact fallback labeling is not acceptable.

When a task touches a course folder, the owning course agent's context takes priority for substance. For example, work inside `GPEC 446 - QM3 - Valasquez/` should load Tyche's definition and memory before editing.

## Edgar-Facing Temporary Outputs

The repo-root `edgar/` folder is a temporary landing zone for files Edgar wants to inspect before Claudia sorts them into durable homes. When Edgar asks for user-facing summaries for a requested day, next-day packets, or similar collect-first workflows, Codex agents may write those outputs to `edgar/` with clear filenames. Durable course-specific copies can later be moved or copied into the proper course folder, usually `[Course Folder]/Study Guides/`, during end-of-day sorting.

Do not move active summary files that already live in course folders unless Edgar explicitly asks for that cleanup.

## Save Protocol

In Codex, "save" means:

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

Claude harness skills and slash commands are not active in this workspace. Codex should use the local file-based procedures in this document.

## Connector and Tool Fallbacks

Use Codex connectors/plugins when available:

- Gmail tasks: Gmail connector.
- Google Calendar tasks: Google Calendar connector.
- Google Drive, Docs, Sheets, Slides tasks: Google Drive connector.
- GitHub tasks: GitHub connector or `gh`.
- Browser testing: Browser Use plugin or local browser tooling.
- Documents, presentations, spreadsheets: corresponding Codex plugins and local scripts.

If a connector is unavailable, use local files and CLI fallbacks where possible, and clearly state what could not be verified. This connector fallback rule applies inside the owning agent's work or to non-agent plumbing. It does not override the delegation rule by letting Claudia perform agent-owned specialist work herself.

## New Agent Onboarding

New agent definitions must be written to `_claudia/agent_definitions/<name>.md`.

Register the agent in `_claudia/system/manifest.json` with:

- `definition`: neutral Codex-compatible path.
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
