---
name: agent-memory
description: All agents must maintain persistent memory files (context, feedback, task log) and update them after major tasks and feedback
applies_to: all agents
---

# Agent Memory Protocol

Every agent in the Claudia system maintains persistent memory across sessions. This ensures continuity, prevents repeated mistakes, and allows agents to improve over time.

## Required Files

Every agent must have the following files in their persistent memory folder:

### 1. `AGENT_CONTEXT.md`
What the agent knows about its domain. For course agents: professor tendencies, course arc, key themes, grading structure, cross-course links. For non-course agents: domain knowledge, operational patterns, and workspace awareness.

**When to update:** After every major work session. Append new information; do not overwrite existing content unless correcting an error.

### 2. `FEEDBACK.md`
A running log of corrections and confirmed good approaches from Edgar or Claudia. This is the most important file for improving over time.

**When to update:** Immediately after receiving feedback, whether a correction or a confirmation that something worked well.

**Entry format:**
```
### [DATE] — [Topic]
**Type:** correction | confirmation
**What:** [What was wrong or right]
**Why:** [Why it matters]
**Rule going forward:** [What to do differently or keep doing]
```

### 3. `TASK_LOG.md`
A brief log of major completed tasks. Prevents duplicate work and gives continuity across sessions.

**When to update:** After completing any major task (summarizing readings, prepping assignments, running analysis, etc.). Keep entries concise.

**Entry format:**
```
### [DATE] — [Task Title]
**Requested by:** Claudia | Edgar
**What was done:** [1-2 sentence summary]
**Output:** [file path or "returned to Claudia"]
**Notes:** [anything worth remembering for next time]
```

### 4. `ASSIGNMENTS.md` (course agents only)
Deadline and deliverable tracker. Update whenever a new assignment is mentioned or a status changes.

## Where Files Live

- **Course agents:** `[Course Folder]/_agent/`
- **Non-course agents:** `_claudia/agents/<agent-name>/`

## Workflow

1. **Before starting work:** Read `AGENT_CONTEXT.md` and `FEEDBACK.md` to load your memory and avoid past mistakes.
2. **During work:** Apply lessons from feedback. Follow confirmed good patterns. Avoid corrected bad patterns.
3. **After completing a major task:** Append to `TASK_LOG.md`.
4. **After receiving feedback:** Append to `FEEDBACK.md` immediately. If the feedback changes how you understand the course or domain, also update `AGENT_CONTEXT.md`.
