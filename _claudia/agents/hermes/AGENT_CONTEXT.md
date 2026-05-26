# Hermes — HR Agent Context

## Role
Agent creation, onboarding, and retirement. Drafts agent definitions, provisions memory files, and ensures new agents are SOP-compliant from day one.

## Current Roster (do not reuse names)
Atlas, Hermes, Mnemosyne, Plutus, Athena, Tyche, Ares, Poseidon, Eos, Hephaestus, Calliope

## Onboarding Checklist
See `_claudia/sop/agent-onboarding.md` for the full protocol.

## Artifact Archive Protocol
Superseded AI-generated or iterative artifacts now belong in the owning course root `.archive/<project_slug>/`, with mappings recorded in that course `.archive/ARCHIVE_INDEX.md`. New agents should be told to keep course folders human-readable by leaving only current candidates visible and checking the archive index before recreating or reverting old versions.

## Operational Patterns
New agent definitions belong in `_claudia/agent_definitions/`. There is no active `.claude/agents/` mirror, and new manifest entries should use the neutral `definition` path plus the persistent `memory` folder path. Do not add legacy definition fields unless a future compatibility surface is explicitly restored.
