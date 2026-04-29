---
name: agent-onboarding
description: When a new agent is created, Hermes must provision all required persistent memory files before the agent begins work
applies_to: Hermes (and any agent creating new agents)
---

# Agent Onboarding Protocol

When a new agent is spun up, it must be provisioned with all required persistent memory files before it begins any work. This is Hermes's responsibility.

## Required Steps

### 1. Create the agent definition
Write the canonical agent definition file at `_claudia/agent_definitions/<name>.md` with all standard sections, including a "Standard Operating Procedures" section pointing to `_claudia/sop/`.

### 2. Create the persistent memory folder

- **Course agents:** `[Course Folder]/_agent/`
- **Non-course agents:** `_claudia/agents/<agent-name>/`

### 3. Provision the following files

Every new agent must have these files created and ready before the agent is activated:

| File | Purpose | Initial Content |
|---|---|---|
| `AGENT_CONTEXT.md` | Domain/course knowledge | Header with agent name, domain, and "To be populated after first session" |
| `FEEDBACK.md` | Corrections and confirmations | Header only, no entries yet |
| `TASK_LOG.md` | Record of completed work | Header only, no entries yet |
| `ASSIGNMENTS.md` | Deadline tracker (course agents only) | Header with sections for Completed, In Progress, Upcoming |

### 4. Update the roster
- Add the new agent to the Agent Roster in `_claudia/system/CLAUDIA.md`
- Update Hermes's own roster list in `_claudia/agent_definitions/hermes.md` to prevent name reuse.

**Permission note:** If Hermes (or any delegated agent) is blocked from editing the definition directory, she must surface the exact one-line patch in her activation summary and flag it for Claudia to apply from the parent session. This sync is not optional, it is the final gate of onboarding. The agent is not considered active until `_claudia/system/CLAUDIA.md` and `_claudia/agent_definitions/hermes.md` reflect the new name.

### 5. Register in the system manifest
- Add the new agent to the `agents` array in `_claudia/system/manifest.json`
- Include: name, type (course or utility), role, model, canonical definition path, memory path, and course code (if course agent)

### 6. Confirm to Claudia
Return to Claudia with:
1. Agent name and mythology note
2. Files created (full paths)
3. Briefing summary
4. Activation note (how to invoke)
