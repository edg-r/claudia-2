---
type: workflow-log
updated: 2026-04-28
---

# Workflow Log

Running log of decisions, patterns, and changes made to the Claudia system. Append new entries at the top.

---

## 2026-04-28 — Syllabus Deadline Pipeline Checkpoint

**Status:** Local checkpoint commit created: `625e060 Standardize syllabus deadline pipeline`.

**Saved in commit:** Five course-owned `Course Admin/syllabus_extracted.md` files; normalized deadline data contract and extraction template; assignment schema/dashboard support; corrected Apr 27/Apr 28 dispatches; Eos, Mnemosyne, Hephaestus, Plutus, and Tyche task-memory updates; `_claudia/claudia.db` checkpoint.

**Push state:** Push was interrupted by the user while running. `main` remained ahead of `origin/main` afterward, so remote sync still needs to be retried.

**Known continuation point:** Mnemosyne normalization partially completed before stream disconnect. Dashboard-critical rows are present for GPPS 463 LD10 due Apr 28 at 17:00, GPCO 403 Concept Check 3 due Apr 28 at 23:59, and GPCO 410 ORANGE memo due Apr 29 at 11:00. Remaining cleanup includes adding future GPPS 463 discussion-post rows for LD11, LD14, LD15, LD16, LD18, and LD19; verifying GPPS 444 oral-presentation confidence; and reviewing any course-agent ambiguities such as GPCO 403 Concept Check 5 date discrepancy.

**Unrelated dirty files left untouched:** `.vscode/settings.json`; GPCO 410 agent memory files; GPEC 446 Homework 1 `.RData` and `.Rhistory`; `_claudia/agents/calliope/TASK_LOG.md`.

---

## 2026-04-12 — Initial Setup

**Built:**
- Full agent roster: Atlas, Hermes, Mnemosyne, Plutus, Athena, Tyche, Ares, Poseidon
- SQLite database at `_claudia/claudia.db` — 6 tables, 5 courses seeded
- `_agent/` context folders for all courses
- 14 skills ported from Cowork desktop app + Obsidian vault
- Obsidian vault moved to `knowledge/obsidian/` (from inbox)
- 14 key Obsidian notes indexed into database
- Memory system initialized at `_claudia/memory/`

**Pending:**
- Parse syllabi PDFs to populate assignments and readings tables
- Build `_agent/AGENT_CONTEXT.md` files for each class agent
- Set up daily briefing skill
- Add remaining Obsidian notes to file index
