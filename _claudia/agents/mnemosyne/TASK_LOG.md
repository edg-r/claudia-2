# Mnemosyne — Task Log

Record of major completed tasks. Read to avoid duplicate work.

<!-- No entries yet. Append new tasks below this line. -->

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
