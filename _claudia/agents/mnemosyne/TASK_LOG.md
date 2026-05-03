# Mnemosyne — Task Log

Record of major completed tasks. Read to avoid duplicate work.

<!-- No entries yet. Append new tasks below this line. -->

## 2026-04-23 — Planning Brief for Thu 4/23 + Fri 4/24
**Requested by:** Claudia
**What was done:** Compiled a structured two-day planning brief covering QM3 HW1 status, assignments due within 7 days, class schedule for Thu/Fri, and existing Google Calendar events.
**Output:** Structured brief returned to Claudia in chat.

### 2026-04-29 — Current Academic Action Checklist DB Scan
**Requested by:** Claudia / Edgar
**What was done:** Queried `_claudia/claudia.db` for pending, overdue, upcoming, and recurring academic obligations as of 2026-04-29 America/Los_Angeles. Crosswalked assignment rows to course owners and treated readings as undated pending backlog by course/week.
**Output:** Relay-ready checklist returned to Claudia in chat.
**Notes:** Hard-dated urgent items are GPCO 410 ORANGE memo due 2026-04-29 11:00, overdue GPPS 463 LD9/LD10 discussion posts, and overdue GPCO 403 Concept Checks 2/3. Pending readings lack due-date fields, so they should be interpreted through course schedule context before dispatching reading work.

## 2026-04-23 — Readings-Due-This-Week Inventory (Mon 4/20 - Sun 4/26)
**Requested by:** Claudia
**What was done:** Inventoried readings due across all five courses for the week of Apr 20-26. Classified each against existing summaries and flagged citation weight. Prioritized three ANCHOR readings (Walter Ch. 2, Bueno de Mesquita et al., Fearon) plus secondary (Herrmann, Tetlock, Visser) and noted missing Cederman PDF.
**Output:** Gap list returned to Claudia in chat.

### 2026-04-15 — Readings Due Today Theory-Reference Summary
**Requested by:** Edgar
**What was done:** Queried the Claudia database and checked official course syllabi/calendar context for readings due Wednesday, April 15, 2026. Applied `_claudia/skills/theory-reference-pdf.md` as a Markdown structure, producing one concise page each for GPCO 403, GPCO 410, GPPS 444, and GPPS 463. Resolved a GPCO 403 mismatch by following the official syllabus and lecture materials over the database's Week 3 PPP label.
**Output:** `_claudia/study_guides/2026-04-15_readings_due_today_theory_reference.md`
**Notes:** GPEC 446 was excluded because no April 15 class reading was identified. GPCO 403 textbook text was not locally available; summary was calibrated from the syllabus and Week 3 lecture PDFs.

## 2026-04-14 — 14-Day Assignment Sweep and Week 3 Reading Page-Count Report
**Requested by:** Claudia (following daily briefing; Edgar asked for DB scan for assignments and readings plus theory-reference-pdf candidates)
**What was done:** Queried `_claudia/claudia.db` for all assignments due between Apr 14 and Apr 28 across all five Spring 2026 courses and compiled a markdown report. Surfaced 7 assignments in window, with two 25%-weight items (GPPS 463 Midterm 1 on Apr 20, GPEC 446 Homework I on Apr 26) flagged as highest-stakes. Pulled Week 3 readings by course with page counts where recorded: GPCO 410 (110 pp: Fearon, Morrow, Powell, Yetiv, Saddam's Delusions), GPEC 446 (49 pp: Angrist & Pischke Ch 3), GPPS 444 (41 pp: Parker Ch 4-5, IW intro), GPPS 463 (65 pp: Dell & Olken, Stubbs 1999, Acemoglu). GPCO 403 textbook pages not in DB — flagged as a data gap; estimated true weekly total is 280-310 pages vs 265 recorded. Then read `_claudia/skills/theory-reference-pdf.md` and evaluated each Week 3 reading against the skill's fit criteria. Shortlisted five high-value candidates (Fearon, Powell, Morrow, Dell & Olken, Stubbs 1999) with brief rationale each, and explicitly excluded quantitative methods readings, news pieces, and pure case-history chapters as poor fits.
**Output:** Full markdown report returned to Claudia in chat; not written to a standalone file (worth committing to `_claudia/dispatches/` or similar if this becomes a recurring sweep).
**Notes:** The daily-briefing skill does not currently scan the DB for assignments and readings — Edgar flagged this as a gap. A future task should fold a DB sweep step into `_claudia/skills/daily-briefing.md` so Eos surfaces upcoming assignments and page counts each morning without a separate Mnemosyne dispatch.

## 2026-04-13 (afternoon) — Infrastructure Scaffold, Assignment DB Update, and Grade Entry
**Requested by:** Claudia (session close)
**What was done:** Assisted Claudia with a full afternoon work session covering two domains. Infrastructure: `_claudia/system/manifest.json` was created as the machine-readable registry of all 10 agents, 5 courses, 15 skills, and 3 SOPs. Supporting files `_claudia/system/README.md` and `AGENTS.md` were created/rewritten for dual Claude Code + Codex use. `CLAUDE.md` was updated to document the system layer. `_claudia/sop/agent-onboarding.md` was updated with step 5 requiring Hermes to register new agents in the manifest. Assignment DB: added GPPS 463 LD5 (due Apr 13) and LD6 (due Apr 14) discussion posts. GPCO 410 analytic memo dates confirmed (BLUE Apr 8, ORANGE Apr 29, PURPLE May 20). GPCO 410 data memos set to three specific rows (Interstate Conflict, Civil War, Regime Type), all due May 15. Grades recorded: GPCO 403 CC1 14.1/17, GPPS 463 LD4 discussion 2/2, LD3 attendance 1/1, LD4 attendance 0/1 (flagged). GPEC 446 midterm corrected to May 5. GPPS 463 LD2 discussion post inserted as completed. Dashboard regenerated to reflect all changes.
**Output:** DB changes committed in-session; dashboard.html regenerated
**Notes:** Three open flags for Edgar: (1) GPPS 463 LD4 attendance graded 0/1 -- may be Canvas error or real absence; (2) GPCO 410 data memos labeled 10% each but syllabus says "choose 1" -- clarify with Prather; (3) GPCO 403 Concept Check 5 date discrepancy Jun 1 vs Jun 2 -- confirm with Handley or Canvas.

## 2026-04-13 — Full Syllabus Audit of All 5 Courses
Comprehensive audit of all five Spring 2026 syllabi against the assignments table (32 rows total after changes). Two changes made:
- UPDATED GPEC 446 Midterm (id=11): corrected due_date from 2026-05-06 (Wednesday) to 2026-05-05 (Tuesday). Syllabus explicitly states "Tuesday, Week 6" — Week 6 Tuesday = May 5. Notes updated accordingly.
- INSERTED GPPS 463 Discussion Post LD2 (id=32): "What explains the rise & fall of the ancient kingdoms of SE Asia?" — due Apr 1, marked completed. Visible in Canvas export as "Apr 1, 2pts."
No changes needed for GPCO 403 (all 9 rows correct), GPCO 410 (all 8 rows correct), GPPS 444 (both rows correct), or GPPS 463 recurring items.

## 2026-04-13 — Assignment DB Audit and Update (Email Findings)
Processed Canvas email findings and conducted DB audit. Changes made:
- ADDED assignments id=27 (GPPS 463 LD5 discussion post, due Apr 13) and id=28 (GPPS 463 LD6 discussion post, due Apr 14 — confirmed via Gmail email 19d86cb4a16562fc).
- REPLACED generic Data Memo row (id=16) with three specific rows: id=29 Interstate Conflict (COW), id=30 Civil War (PRIO), id=31 Regime Type (Polity IV), all due May 15 per Prather Canvas email.
- UPDATED analytic memo due dates: id=14 BLUE to Apr 8 (last window option), id=15 ORANGE to Apr 29, id=17 PURPLE to May 20.
- UPDATED recurring assignment notes for ids 20, 25, 26 (GPPS 444 quizzes, GPPS 463 discussion posts/attendance); left due_date NULL as appropriate.
- RECORDED 4 grade entries in grades table: GPCO 403 CC1 (14.1/17), GPPS 463 LD4 discussion (2.0/2.0), LD3 attendance (1.0/1.0), LD4 attendance (0.0/1.0 — flagged).
- Also updated assignment id=1 status to completed and grade to 14.1/17.

## 2026-04-13 (evening) — Embedding Coverage Expansion + files.indexed Fix
**Requested by:** Claudia
**What was done:** Identified that the files table had 76 course files on disk not registered in the DB (relative vs absolute path mismatch between files.path and embeddings.source_path was also discovered). Inserted 76 missing files into the files table with correct course_id assignments. Ran full embedding index run: 73 new files indexed, 3,087 new chunks added. Total coverage rose from 60/68 to 133/144 indexable files (92%). 11 files remain unindexed: 8 are confirmed scanned/image PDFs with no extractable text, 1 is AES-encrypted (RAND Research Report), and 2 others failed text extraction. Fixed files.indexed column: previously 841/842 were marked indexed (inaccurate); now set to 1 only where absolute path appears in embeddings.source_path (134 files), 0 for the rest (784 files). Dashboard regenerated.
**Per-course final counts:** GPCO 403: 27 files, 205 chunks | GPCO 410: 54 files, 2,326 chunks | GPEC 446: 12 files, 1,835 chunks | GPPS 444: 14 files, 1,066 chunks | GPPS 463: 25 files, 977 chunks
**Notes:** Mastering Metrics textbook is indexed twice (duplicate path entries for same PDF in GPEC 446). RAND report encryption requires cryptography package upgrade to embed.

## 2026-04-13 — Dashboard Embedding Stats Update
Updated `_claudia/dashboard.html` with current embedding stats. Changes: (1) Embeddings Coverage section: corrected overall from "60/842 files (7%)" to "60/68 files (88%)" and added total chunk count (3,323); (2) Added "Chunks" column to per-course coverage table with values GPCO 403: 20, GPCO 410: 948, GPEC 446: 923, GPPS 444: 1,061, GPPS 463: 370; (3) Updated subtitle datestamp. Summary card (3323 chunks, 60 files) was already accurate — no change needed there.

## 2026-04-13 — Embedding Index Run (All Courses)
Ran the embedding indexing pipeline for all five courses. All files were already current from a prior run (2026-04-13 07:26:31). Final status: 3,323 total chunks, 60 unique files indexed out of 68 indexable files in the DB (coverage 60/68). Eight files remain unindexed — these are scanned PDFs with no extractable text (confirmed "skipped - no text" messages during indexing). The gap is expected and not an error.

## 2026-04-12 — Workspace Inventory Query
Full database and folder scan. Confirmed: 5 courses, 842 tracked files, 77 readings (all pending), 26 assignments across 4 courses, 0 grades entered, 0 agent_logs for Mnemosyne yet. Course folders all present with _agent subdirectories. GPEC 446 and GPPS 444 have no direct assignment entries for GPEC 446's QM3 content or GPPS 444's oral presentation status.

## 2026-04-20 — Open-Assignments Sweep + HW1/Orange Reading Page Counts
Ran two cross-course queries. First: full open-assignments rundown across GPCO 403, GPCO 410, GPEC 446, GPPS 444, GPPS 463 sorted by due date for chat-only delivery. DB found well up-to-date; flagged BLUE memo (Apr 8), Data Brief 1 (Apr 17), and Apr 13/14 discussion posts still marked `pending` but confirmed completed per session memory. Added Breitenfeld presentation (Apr 20) from session memory since it wasn't a DB row. Second: page counts for Orange Memo readings (Cederman/Hug/Krebs core = 18pp; full W4-W5 window = 178pp) and QM3 HW1 readings (386 slide-pages across 9 files). The 386 figure was raw slide-pages; Tyche later walked it back to ~244 needed slide-pages after scoping by question. Confirmed HW1 deadline as Sat Apr 25 midnight, not Apr 26 as previously thought.

### 2026-04-27 — Closed Completed Assignment DB Rows
**Requested by:** Edgar
**What was done:** Updated exactly seven stale assignment rows in `_claudia/claudia.db` to `status='completed'` based on agent-log-completed items: GPCO 410 BLUE memo, GPPS 463 LD5/LD6 discussion posts, GPCO 403 Data Brief 1, GPPS 444 Oral Presentation, GPPS 463 Midterm Exam 1, and GPEC 446 Homework I. Queried assignments due on 2026-04-27 afterward.
**Output:** Returned to Edgar in chat.
**Notes:** Three requested labels used shorthand; matched to stored rows by course and due date: `Analytic Memo — BLUE (choose 1)`, `Discussion Post for Lecture Day 5...`, and `Discussion Post for Lecture Day 6...`. No assignments were due on 2026-04-27 in the DB.

### 2026-04-27 — Inbox Knowledge Sorting
**Requested by:** Edgar
**What was done:** Sorted five inbox items into `knowledge/obsidian/` after inspecting filenames and representative content. Added AI-researched provenance via Markdown frontmatter or adjacent metadata notes, and updated matching `files` records in `_claudia/claudia.db`.
**Output:** Moved files under `knowledge/obsidian/000 AI Analysis/AI Tools/`, `knowledge/obsidian/000 AI Analysis/GPCO 410/`, and `knowledge/obsidian/Notes/`.
**Notes:** Left `inbox/.DS_Store` untouched because the scope prohibited deletion and it is not a knowledge item. `Claude.pdf` was image-based; first rendered page identified it as the AI Workflow Reconnaissance report.
### 2026-04-28 — Deadline Data Contract and Assignment Schema Upgrade
**Requested by:** Claudia / Edgar
**What was done:** Added the normalized deadline data contract and upgraded `_claudia/claudia.db` assignments with structured deadline metadata fields. Backfilled existing rows conservatively with timezone, source/confidence, date kind, recurring flags, recurrence rules, selected explicit due times, and `last_verified_at`.
**Output:** `_claudia/system/deadline-data-contract.md`; `_claudia/system/syllabus-extraction-template.md`; `_claudia/claudia.db`
**Notes:** Course agents should write `Course Admin/syllabus_extracted.md`; Mnemosyne owns DB normalization; Hephaestus owns dashboard/tooling. Current data remains mostly `legacy_db` until course agents re-run extraction against the new contract.

### 2026-04-28 — Syllabus Extraction Normalization Pass
**Requested by:** Claudia / Edgar
**What was done:** Normalized `_claudia/claudia.db` from the five course-owned `Course Admin/syllabus_extracted.md` files after course-agent dispatches stalled and Claudia used the explicit local fallback. Updated source paths, due times, confidence/date-kind metadata, recurring rules, and added missing GPPS 463 LD8/LD9/LD10 discussion-post rows.
**Output:** `_claudia/claudia.db`; `_claudia/dashboard.html`
**Notes:** Today's dashboard-critical rows now include GPPS 463 LD10 discussion post due 2026-04-28 17:00, GPCO 403 Concept Check 3 due 2026-04-28 23:59, and GPCO 410 ORANGE memo due 2026-04-29 11:00.

### 2026-04-29 — Checklist Status Refresh and Midterm Priority Query
**Requested by:** Edgar
**What was done:** Updated five handled checklist rows in `_claudia/claudia.db`: GPCO 403 Concept Checks 2 and 3 marked `completed`; GPPS 463 LD9 and LD10 discussion posts plus GPCO 410 ORANGE memo marked `submitted`. Stamped `submitted_at` and `last_verified_at` with the current local time, then queried active upcoming assignments with midterms prioritized.
**Output:** `_claudia/claudia.db`; priority list returned to Claudia in chat.
**Notes:** Active near-term priority is now midterms first: GPCO 410 and GPCO 403 on 2026-05-04, GPEC 446 on 2026-05-05, GPPS 463 Midterm Exam 2 on 2026-05-11.

### 2026-04-30 — Reference Sheet Visual Preference
**Requested by:** Edgar
**What was done:** Persisted Edgar's cross-course preference that future reference sheets should treat imagegen-created conceptual visuals/infographics as a standard component when useful and feasible, following the QM3 v1.3.0 reference-sheet pattern.
**Output:** `_claudia/memory/preferences.md`
**Notes:** Preference applies across courses and should be checked before future lecture-to-reference or theory-reference sheet builds.
### 2026-05-02 - Central Artifact Archive Recommendation
**Requested by:** Claudia
**What was done:** Recommended the initial archive approach, then Edgar corrected the design to course-local archives under `[Course Folder]/.archive/<project_slug>/` with `[Course Folder]/.archive/ARCHIVE_INDEX.md` as the human-readable index.
**Output:** Returned to Claudia; protocol recorded in `_claudia/agents/mnemosyne/AGENT_CONTEXT.md`
**Notes:** Mnemosyne owns archive discovery conventions and should search the owning course archive index before broad file scans.
