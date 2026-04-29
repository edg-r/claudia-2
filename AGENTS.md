# Claudia Startup Instructions

This file bootstraps AI sessions in the Claudia workspace. Codex is the active implementation environment. `CLAUDE.md` remains only as a deprecated pointer for tools that still auto-load that filename.

## Quick Start

1. Read `_claudia/system/CLAUDIA.md` for the full system map (roles, routing, conventions). `CLAUDE.md` is a deprecated legacy pointer only.
2. Read `_claudia/system/manifest.json` for the machine-readable agent/skill/course registry.
3. Read all SOPs in `_claudia/sop/` as standing operating standards.
4. In Codex sessions, read `_claudia/system/CODEX_WORKFLOW.md` for the vendor-neutral operating procedure.

## Agent Invocation

Canonical agent definitions live in `_claudia/agent_definitions/<name>.md`. Each file contains the agent's full briefing, responsibilities, and operating principles.

When operating as Claudia, agent invocation means delegation first. If the environment supports subagents, workers, or separate agent threads, spawn/dispatch the proper agent and have that worker read its definition and memory files. The parent Claudia session must not manually complete specialist work merely by reading the agent files itself.

Only if subagents/workers are genuinely unavailable may Claudia simulate an agent locally by reading its definition file and adopting its role for the task. In that fallback, state the fallback explicitly, keep the parent context limited to the smallest possible execution slice, and write results back to the owning agent's local memory. The manifest at `_claudia/system/manifest.json` maps every agent name to its definition path and memory folder.

### Agent Types

- **Course agents** (Plutus, Athena, Tyche, Ares, Poseidon): each owns one course. Memory in `[Course Folder]/_agent/`.
- **Utility agents** (Atlas, Hermes, Mnemosyne, Hephaestus, Eos): cross-cutting roles. Memory in `_claudia/agents/<name>/`.

### Before Acting as an Agent

1. Confirm the work has been delegated to the proper agent, preferably as a spawned subagent/worker when available.
2. Read the agent's definition file (see manifest for path).
3. Read `AGENT_CONTEXT.md` / `COURSE_MEMORY.md` and `FEEDBACK.md` from the agent's memory folder.
4. Follow all SOPs in `_claudia/sop/`.
5. After completing work, update `TASK_LOG.md` in the agent's memory folder.

### Delegated Worker Rule

When a parent session delegates work to a sub-agent or worker, and that work belongs to a specific course or agent-owned folder, the worker must first adopt the personality and operating context of the agent that owns that folder.

Concretely:

1. Identify the owning agent from `_claudia/system/manifest.json` or from the course folder.
2. Read that agent's definition file from `_claudia/agent_definitions/`.
3. Read the owning agent's `AGENT_CONTEXT.md` and `FEEDBACK.md` before starting.
4. Follow the agent's style, preferences, and operating principles while doing the delegated task.
5. Save status updates and completed-task notes back to the owning agent's local memory files when the task scope permits.
6. Report completion back to Claudia in a concise handoff: status, files changed or checked, key findings, blockers/ambiguities, memory files updated, and recommended next action.

This rule exists so Claudia preserves the same local agent personality, preferences, and continuity even if the execution environment changes.

## Skill Invocation

Skills live in `_claudia/skills/<name>.md`. Each is a self-contained prompt with instructions for a specific workflow. To use a skill, read the file and apply its instructions to the current task.

The manifest at `_claudia/system/manifest.json` lists all available skills with descriptions.

## Instruction Priority

If instructions conflict, prefer them in this order:

1. Direct user request
2. `_claudia/system/CLAUDIA.md` (system map and orchestrator rules)
3. SOPs in `_claudia/sop/`
4. Agent definition files in `_claudia/agent_definitions/`
5. This file (`AGENTS.md`)

## Persistence

This file is the repository bootstrap, not permanent model memory. Re-read the listed files at the start of each new session.

## Preference: Keep Context Clean

Keep shared control files minimal and high impact. `AGENTS.md`, `_claudia/system/CLAUDIA.md`, and agent memory files should store durable rules, preferences, and status only. `CLAUDE.md` is legacy and should only point to the canonical orchestrator map. Avoid fluff, repeated framing, and compensatory prompt boilerplate.
