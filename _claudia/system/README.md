# System Layer

Machine-readable configuration for the Claudia orchestrator. These files allow Codex or future tools to bootstrap the workspace consistently.

## Files

- `manifest.json` -- complete registry of agents, courses, skills, and SOPs. This is the single source of truth for the workspace graph. When a new agent is created or a skill is added, this file must be updated.
- `CLAUDIA.md` -- canonical vendor-neutral orchestrator map. `CLAUDE.md` at the repo root is only a deprecated compatibility pointer.
- `CODEX_WORKFLOW.md` -- Codex-first operating procedure for agent invocation, save behavior, connector fallback, and migration smoke tests.

## How to use

At session start, read `manifest.json` to discover:
- Which agents exist and where their definitions + memory live
- Which courses are active and their folder paths
- Which skills are available and how to invoke them
- Which SOPs apply to all agents

## Maintenance

When Hermes onboards a new agent, the final step is adding it to `manifest.json`. When a new skill is created, add it here too. This keeps the manifest as the single source of truth that Codex can rely on.
