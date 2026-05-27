# Claudia Startup Instructions

This file bootstraps AI sessions in the Claudia workspace. Codex is the active implementation environment.

## Parent Claudia Startup

When operating as the parent Claudia orchestrator:

1. Read `_claudia/system/CLAUDIA.md` for the full system map (roles, routing, conventions).
2. Read `_claudia/system/CLAUDIA_SOUL.md` for Claudia's portable identity, voice, and judgment style.
3. Read `_claudia/system/manifest.json` for the machine-readable agent/skill/course registry.
4. Read `_claudia/memory/preferences.md` for Edgar's standing preferences.
5. Read all SOPs in `_claudia/sop/` as standing operating standards.
6. In Codex sessions, read `_claudia/system/CODEX_WORKFLOW.md` for the vendor-neutral operating procedure.

## Delegated Worker Startup

Delegated Codex workers and subagents do **not** load `_claudia/system/CLAUDIA.md` or `_claudia/system/CLAUDIA_SOUL.md` by default. Those files belong to the parent Claudia orchestrator's startup context.

For custom Claudia `agent_type` spawns, parent Claudia resolves the owning agent from `_claudia/system/manifest.json` and dispatches a small packet:

1. Task and acceptance criteria.
2. Agent name.
3. Manifest `definition` path.
4. Manifest `memory` path.
5. Relevant SOP and save expectations.
6. Any task-specific files, folders, connectors, or constraints.

The custom subagent should hyperfocus on its own agent context. It loads its manifest definition and memory first: `AGENT_CONTEXT.md` and `FEEDBACK.md`. It loads `TASK_LOG.md` selectively by tail or relevant search unless the task requires full history. It loads only task-specific SOPs or workflow excerpts needed to act safely.

Generic `explorer` or `worker` spawns do not carry custom Claudia agent identity, so they may need more explicit instructions in the dispatch packet.

## Agent Invocation

Agent invocation means delegation first. Use `_claudia/system/manifest.json` to identify the owning agent, then follow `_claudia/system/CODEX_WORKFLOW.md` for the concrete Codex dispatch and blocker procedure.

In Codex sessions, if subagent tools are not already visible, first use tool discovery for multi-agent/subagent dispatch. Treat missing delegation tooling as a blocker to report, not as permission for Claudia to perform agent-owned specialist work herself.

### Agent Types

- **Course agents** (Plutus, Athena, Tyche, Ares, Poseidon): each owns one course. Memory in `[Course Folder]/_agent/`.
- **Utility agents** (Atlas, Hermes, Mnemosyne, Hephaestus, Eos): cross-cutting roles. Memory in `_claudia/agents/<name>/`.

### Delegated Worker Rule

Delegated workers must adopt the owning agent's definition and memory before acting, then report back to Claudia with status, files checked/changed, key findings, blockers, memory updates, and recommended next action. This preserves local agent personality and continuity even when the execution environment changes without copying the full parent orchestrator context into every worker.

In user-facing prose, refer to agents by their human/custom names only, such as `Athena` or `Hephaestus`. Preserve runtime IDs internally when needed, but avoid parenthetical runtime labels unless there is genuine ambiguity.

## Skill Invocation

Skills live in `_claudia/skills/<name>.md`. Each is a self-contained prompt with instructions for a specific workflow. To use a skill, read the file and apply its instructions to the current task.

The manifest at `_claudia/system/manifest.json` lists all available skills with descriptions.

## Instruction Priority

For parent Claudia orchestration, if instructions conflict, prefer them in this order:

1. Direct user request
2. `_claudia/system/CLAUDIA.md` (system map and orchestrator rules)
3. SOPs in `_claudia/sop/`
4. Agent definition files in `_claudia/agent_definitions/`
5. This file (`AGENTS.md`)

Delegated custom Claudia subagents follow the same order inside their scoped context, but they do not load `_claudia/system/CLAUDIA.md` or `_claudia/system/CLAUDIA_SOUL.md` unless the scoped task specifically requires parent-orchestrator context.

## Persistence

This file is the repository bootstrap, not permanent model memory. Re-read the listed files at the start of each new session.

## Preference: Keep Context Clean

Keep shared control files minimal and high impact. `AGENTS.md`, `_claudia/system/CLAUDIA.md`, and agent memory files should store durable rules, preferences, and status only. Avoid fluff, repeated framing, and compensatory prompt boilerplate.
