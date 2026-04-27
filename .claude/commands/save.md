---
name: save
description: Save session insights to Claudia's memory, prompt subagents used this session to update memory, then commit and push the scoped saved changes. Run before compaction or sign-off.
---

# /save — End of Session Memory Sweep

When Edgar invokes `/save`, Claudia (this orchestrator session) performs a structured memory sweep of the current conversation, then commits and pushes the scoped saved changes to GitHub. The goal is to preserve everything durable, skip everything ephemeral, and leave the current branch backed up without sweeping unrelated dirty work into the commit.

Claudia runs this command herself. It is not delegated to a subagent. Claudia may, however, re-dispatch individual subagents to update their own memory files, which is step 4 below.

## Step 1: Review the conversation with filtering discipline

Scan the session from start to finish. For each moment, ask whether it meets the bar for long-term memory. The bar is the same one already defined in the `auto memory` section of Claudia's system prompt. Save only:

1. **User memories.** New durable facts about Edgar: preferences, routines, study methods, tool stack changes, career context, personal context that will matter across future sessions. Store at `/Users/edgar/.claude/projects/-Users-edgar-Documents-01-Projects-Claudia/memory/user_edgar_profile.md` (append or revise the relevant section) or as a standalone `user_<topic>.md` file if the topic is large enough to warrant its own entry.

2. **Feedback memories.** New corrections or confirmations from Edgar, especially non-obvious ones that override a default behavior. File naming convention: `feedback_<topic>.md`. Examples already on disk: `feedback_writing_style.md`, `feedback_routing_first.md`, `feedback_deliverable_format.md`. If feedback is agent-specific, it also goes into that agent's own `FEEDBACK.md` (see step 4). Cross-agent feedback lives in the project memory folder and is indexed in `MEMORY.md`.

3. **Project memories.** Decisions, new initiatives, infrastructure changes, deadlines, incidents, or state changes that affect how the workspace operates going forward. File naming: `project_<topic>_YYYY-MM-DD.md` for one-off events or `project_session_YYYY-MM-DD.md` for the daily session log (step 2 below).

4. **Reference memories.** External resources Edgar pointed at or that the session surfaced as load-bearing: URLs, citation anchors, specific readings to revisit, tools to evaluate. File naming: `reference_<topic>.md`.

## Step 2: Write the session log

Always produce one session log per `/save` run at:

`/Users/edgar/.claude/projects/-Users-edgar-Documents-01-Projects-Claudia/memory/project_session_YYYY-MM-DD.md`

Use today's date. If a log already exists for today (the session ran in multiple passes), append a new dated section rather than overwriting; preserve earlier prose intact.

Format: full prose, paragraph-form, nuance preserved. No bullet soup. Frontmatter required:

```
---
name: Session Log — YYYY-MM-DD
description: [one-line summary of the session's main threads]
type: project
originSessionId: [session id if known, otherwise omit]
---
```

Read `project_session_2026-04-15.md` as the primary format template and `project_session_2026-04-14.md` as a second reference for tone, length, and level of detail. The prose should capture what was done, who did it, what was decided, what was corrected, what was left open, and any meta-decisions worth preserving. Name files and paths touched in a closing paragraph so the log is self-auditing.

## Step 3: Update MEMORY.md

Open `/Users/edgar/.claude/projects/-Users-edgar-Documents-01-Projects-Claudia/memory/MEMORY.md` and add pointer entries for every new memory file created in steps 1 and 2. Keep the existing format exactly: one bullet per file, link text is the title, em-separator uses a hyphen, short description follows. Example of an existing line:

`- [Session Log — 2026-04-15](project_session_2026-04-15.md) - Calliope onboarding ...`

Do not use emdashes. Use a plain hyphen with spaces around it (the existing file uses this convention).

Place new session-log entries at the top of the session-log section. Place new feedback/user/reference memories in the appropriate sections. If a category header does not exist yet, create one in a logical position.

## Step 4: Update each subagent's memory

For every subagent dispatched during this session, the agent-memory SOP at `_claudia/sop/agent-memory.md` requires three files be kept current:

- `AGENT_CONTEXT.md` if the session revealed new durable domain knowledge for that agent
- `FEEDBACK.md` if Edgar (or Claudia) gave the agent a correction or a confirmation during the session
- `TASK_LOG.md` always, if the agent completed work this session

Paths:

- Non-course agents: `_claudia/agents/<agent-name>/`
- Course agents: `[Course Folder]/_agent/`

Claudia has two ways to execute these updates. Prefer the first when the agent is available and a quick re-dispatch is cheap; prefer the second when the agent is already terminated, the update is mechanical, or cascade termination risk is high.

**Option A: Re-dispatch the agent.** Send a short brief asking the agent to update its own memory files per the agent-memory SOP. Pass the relevant session context so the agent can write its own entries with domain voice intact. This is the cleanest pattern and it matches how the agents normally learn.

**Option B: Claudia patches directly.** If re-dispatch is not available, Claudia writes the patches herself using the format already defined in the SOP. For `FEEDBACK.md`:

```
### YYYY-MM-DD - [Topic]
**Type:** correction | confirmation
**What:** [what was wrong or right]
**Why:** [why it matters]
**Rule going forward:** [what to do differently or keep doing]
```

For `TASK_LOG.md`:

```
### YYYY-MM-DD - [Task Title]
**Requested by:** Claudia | Edgar
**What was done:** [1-2 sentence summary]
**Output:** [file path or "returned to Claudia"]
**Notes:** [anything worth remembering for next time]
```

Note the harness write restriction documented in `feedback_agent_onboarding_roster_sync.md`: subagents cannot write inside `.claude/agents/`. Memory folders at `_claudia/agents/<name>/` are not affected by that restriction, so both options work for the standard memory files.

## Step 5: Commit and push the save scope

After the memory sweep is complete, persist the saved work to GitHub. This step is part of `/save`, but it must be scoped carefully.

1. Inspect the worktree with `git status --short` before staging anything.
2. Identify the save scope: memory files created or edited by this `/save` run, session output files produced or updated during the conversation, and any other files Edgar explicitly asked to include. Do not include unrelated pre-existing dirty files just because they are present in the worktree.
3. If the scope is ambiguous, ask Edgar which files to include. If asking is not possible, leave ambiguous files unstaged and report them in the confirmation.
4. Stage only explicit pathspecs with `git add -- <path> ...`. Do not use `git add -A`, `git add .`, or broad directory staging unless the entire directory is unquestionably inside the save scope.
5. Review the staged set with `git diff --cached --name-only` and `git diff --cached --stat`. If unrelated paths are staged, unstage those exact paths before committing.
6. If there are no scoped changes after the memory sweep, skip the commit and push, then say so in the confirmation.
7. Create a concise, meaningful commit message derived from the session summary. Use an imperative subject line, prefer 50 to 72 characters, and avoid generic subjects like `save`, `update`, or `misc`.
8. Commit the staged files only after the scoped diff looks right.
9. Push the current branch after the commit succeeds. Use the branch's configured upstream when available. If no upstream exists, push the current HEAD to `origin` with upstream tracking only if the remote is clearly the intended GitHub remote.
10. Surface any commit or push failure in the confirmation, including whether files remain staged, whether the commit was created, and whether the push reached the remote.

The `/save` command must never blindly commit unrelated dirty files. A dirty worktree is normal in Claudia; scoped commits are the rule.

## Step 6: Respect all SOPs

Two SOPs govern this run:

1. `_claudia/sop/agent-memory.md` defines the memory file structure and update discipline. Follow it exactly.
2. `_claudia/sop/output-disclosure.md` governs standalone deliverables written during the session. Live `/save` confirmation messages do not need a disclosure block.

## What NOT to save

The filtering discipline matters as much as the saving. Do not write memory entries for:

- One-off task outputs that are already saved elsewhere (a memo draft lives in the course folder, not in memory; memory points to it)
- Restating facts that are already in an existing memory file without adding new information
- Chit-chat, throat-clearing, or acknowledgments that carry no decision weight
- Information that will naturally re-surface next session from the workspace itself (file listings, DB queries, etc.)
- Speculation about future work that has not been committed to; only save decisions and initiatives Edgar has actually greenlit
- Anything Edgar asked Claudia not to remember

When in doubt, ask Edgar before saving. A short "worth saving?" check is better than a bloated memory index.

## Confirmation message

At the end of the run, return to Edgar a short confirmation that lists:

- The session log file path
- Every new or modified memory file (user, feedback, project, reference)
- Every subagent whose memory was updated, with the files touched for each
- The commit hash and branch pushed, or the reason commit/push was skipped or failed
- Anything that was considered but deliberately skipped, with a one-line reason

## Invocation

Edgar runs `/save` before compaction or sign-off. The command is a no-argument trigger; Claudia scans the current session herself. If Edgar wants to scope the save (for example, only feedback, or skip the session log), he can say so in the same message and Claudia honors that scoping.
