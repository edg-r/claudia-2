# Claudia Startup Instructions

This file bootstraps AI sessions in the Claudia workspace. It works for both Claude Code and OpenAI Codex.

## Quick Start

1. Read `CLAUDE.md` for the full system map (roles, routing, conventions).
2. Read `_claudia/system/manifest.json` for the machine-readable agent/skill/course registry.
3. Read all SOPs in `_claudia/sop/` as standing operating standards.

## Agent Invocation

Agent definitions live in `.claude/agents/<name>.md`. Each file contains the agent's full briefing, responsibilities, and operating principles.

To invoke an agent, read its definition file and adopt its role for the task. The manifest at `_claudia/system/manifest.json` maps every agent name to its definition path and memory folder.

### Agent Types

- **Course agents** (Plutus, Athena, Tyche, Ares, Poseidon): each owns one course. Memory in `[Course Folder]/_agent/`.
- **Utility agents** (Atlas, Hermes, Mnemosyne, Hephaestus, Eos): cross-cutting roles. Memory in `_claudia/agents/<name>/`.

### Before Acting as an Agent

1. Read the agent's definition file (see manifest for path).
2. Read `AGENT_CONTEXT.md` and `FEEDBACK.md` from the agent's memory folder.
3. Follow all SOPs in `_claudia/sop/`.
4. After completing work, update `TASK_LOG.md` in the agent's memory folder.

## Skill Invocation

Skills live in `_claudia/skills/<name>.md`. Each is a self-contained prompt with instructions for a specific workflow. To use a skill, read the file and apply its instructions to the current task.

The manifest at `_claudia/system/manifest.json` lists all available skills with descriptions.

## Instruction Priority

If instructions conflict, prefer them in this order:

1. Direct user request
2. `CLAUDE.md` (system map and orchestrator rules)
3. SOPs in `_claudia/sop/`
4. Agent definition files in `.claude/agents/`
5. This file (`AGENTS.md`)

## Persistence

This file is the repository bootstrap, not permanent model memory. Re-read the listed files at the start of each new session.
