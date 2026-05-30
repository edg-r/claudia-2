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

### 2026-05-04 - GPCO 410 Midterm Status Update
**Requested by:** Claudia
**What was done:** Updated assignment id=18 (`GPCO 410` Midterm Exam) in `_claudia/claudia.db` from `pending` to `completed` after Edgar stated the midterm is done. Stamped `submitted_at` and `last_verified_at` as `2026-05-04 19:50:54 PDT` and appended provenance to the row notes.
**Output:** `_claudia/claudia.db`
**Notes:** Verified only the GPCO 410 midterm row changed; Final Exam and other GPCO 410 assignments remain untouched.

### 2026-05-09 - Local Inbox Cleanup
**Requested by:** Claudia / Edgar
**What was done:** Sorted clear local `inbox/` materials into course, admin, and project folders after reading Claudia bootstrap files, Mnemosyne context, SOPs, preferences, filenames, and representative document metadata/text. Left active GPPS 463 `inbox/midterm2/` in place for Poseidon workers, preserved the Rockbox project bundle in place, and wrote an ambiguity report for unsafe items.
**Output:** `_claudia/agents/mnemosyne/inbox_cleanup_ambiguity_report_2026-05-09.md`; `_claudia/claudia.db`; moved files under GPEC 446, GPCO 403, GPCO 410, `admin/`, and `democracy_as_boredom_bbi/`.
**Notes:** Inserted 36 moved-file records into the `files` table and one Mnemosyne `agent_logs` row. Exact GPCO 403 duplicate copies were moved to the course-local archive instead of overwriting visible originals.

### 2026-05-11 - GPCO 410 Regime Type data memo DB status correction
**Requested by:** Claudia / Edgar
**What was done:** Verified that `GPCO 410 - Intl Pol:Sec - Praether/Assignments/Data Memo - Regime Type/` contains a working outline and completed Polity5 Myanmar data pull. Updated `_claudia/claudia.db` assignment id 31 from `pending` to `outlined`, recorded the outline/data-pull note, set `last_verified_at` to `2026-05-11`, and inserted file-index rows for the outline and Myanmar CSV if absent.
**Output:** `_claudia/claudia.db`; `_claudia/dispatches/2026-05-11_daily-dispatch.md`; Obsidian copy at `000 ARCHIVES/Daily/2026-05-11_daily-dispatch.md`
**Notes:** Assignment ids 29 COW and 30 PRIO remain pending because the found artifacts belong to the Regime Type / Polity IV option only.

### 2026-05-11 - GPPS 463 Midterm Exam 2 completion correction
**Requested by:** Edgar
**What was done:** Updated `_claudia/claudia.db` assignment id 23 (`GPPS 463` Midterm Exam 2) from `pending` to `completed` based on Edgar's correction that the exam was completed today. Stamped `submitted_at` and `last_verified_at` as `2026-05-11 09:54:44 PDT` and appended concise provenance to the row notes.
**Output:** `_claudia/claudia.db`
**Notes:** Current-day scan after correction shows the only dated 2026-05-11 GPPS 463 row is now completed; syllabus extraction marks LD13 as an exam/no-reading/no-discussion-post day.

### 2026-05-14 - Academic Admin Sweep
**Requested by:** Claudia / Edgar
**What was done:** Inspected the SQLite schema and queried active assignments/readings/grades for stale or near-term rows as of 2026-05-14. No DB rows were changed because no past-due pending assignment rows had clear durable evidence for closure.
**Output:** Returned to Claudia; no DB changes.
**Notes:** Near-term obligations remain GPCO 410 data memo options due 2026-05-15 17:00, GPCO 403 Concept Check 4 due 2026-05-18 23:59, GPCO 410 Analytic Memo PURPLE due 2026-05-20 11:00, and GPEC 446 Homework II due 2026-05-23 23:59. Close the unused GPCO 410 data memo options only after Edgar submits or clearly chooses the Regime Type option.

### 2026-05-14 - Data Memo DB Status Cleanup Fallback
**Requested by:** Claudia / Edgar
**What was done:** After the delegated Mnemosyne worker timed out, Claudia invoked Mnemosyne locally as an explicit fallback and updated `_claudia/claudia.db`: assignment ids 29 and 30 were changed from `pending` to `alternate_option`, and assignment id 31 was changed from `outlined` to `drafting` based on the active `Blue Memo v1.docx` in the Regime Type assignment folder.
**Output:** `_claudia/claudia.db`
**Notes:** No row was marked submitted or completed. Regime Type remains the live GPCO 410 data memo due 2026-05-15 17:00; COW and PRIO are inactive alternatives because the prompt requires choosing one data memo.

### 2026-05-15 - Actual Finance Dashboard Schema Inspection
**Requested by:** Claudia / Edgar
**What was done:** Inspected `My-Finances-cleaned-actual-export-v3/db.sqlite` read-only for the dashboard build. Identified the Actual Budget-style schema, row counts, account balance fields, transaction date and amount formats, reliable category join path, budget tables, and SimpleFIN sync-related fields.
**Output:** Returned schema notes to Claudia; no DB changes.
**Notes:** `transactions.date` uses integer `YYYYMMDD`; amounts are cents; direct joins from `transactions.category` to `categories.id` are more reliable for this cleaned DB than `v_transactions` category mapping. The live transaction range is 2025-09-18 through 2026-05-14.

### 2026-05-15 - GPCO 410 Regime Type data memo completion
**Requested by:** Edgar
**What was done:** Updated `_claudia/claudia.db` assignment id 31 (`Data Memo — Regime Type (Polity IV)`) from `drafting` to `completed` after Edgar confirmed the data memo is done. Stamped `submitted_at` and `last_verified_at` as `2026-05-15 12:45 PDT` and inserted a matching `agent_logs` row.
**Output:** `_claudia/claudia.db`; `GPCO 410 - Intl Pol:Sec - Praether/_agent/ASSIGNMENTS.md`
**Notes:** Assignment ids 29 and 30 remain `alternate_option`; only the selected Regime Type data memo row was closed.

### 2026-05-17 - T-Mobile Inbox Plan Scan
**Requested by:** Claudia / Edgar
**What was done:** Searched local `inbox/` for T-Mobile/account/plan documents by filename and content, then extracted account, plan, line, equipment, service, and contact details from the sole matching bill summary PDF.
**Output:** Returned to Claudia; no files moved or deleted.
**Notes:** `inbox/May 17, 2026BillSummary.pdf` lists account 963822429 with 10 voice lines and 1 wearable, but does not map phone numbers to member names or include cancellation/transfer policy details. Edgar must verify line ownership and release/remove terms with T-Mobile before acting.

### 2026-05-17 - Harvey Sociology PDF Course Classification
**Requested by:** Claudia / Edgar
**What was done:** Classified `inbox/harvey-2023-everyone-thinks-they-re-special-how-schools-teach-children-their-social-station.pdf` against active Claudia courses using PDF metadata/text, manifest course ownership, course agent contexts, SQLite `courses`/`readings`/`files` rows, course-admin syllabus extracts, and the prior inbox ambiguity report.
**Output:** Returned to Claudia; no files moved and no study guide generated.
**Notes:** No clear active course owner found. The article is an American Sociological Review piece on school socialization, social station, inequality, and social reproduction; it does not match current Spring 2026 course reading rows or course-admin extracts. Keep in inbox or ask Edgar whether to file under `knowledge/obsidian/`, a research project, or another non-course reference area.

### 2026-05-21 - GPCO 410 PURPLE/NATO memo submission status
**Requested by:** Claudia / Edgar
**What was done:** Inspected the `assignments`, `courses`, and `agent_logs` schemas, then joined `assignments` to `courses` to find the matching GPCO 410 PURPLE/NATO memo row. Updated only assignment id 17 (`Analytic Memo — PURPLE (choose 1)`) from `pending` to `submitted`, stamped `submitted_at` and `last_verified_at` as `2026-05-21 12:23:59 PDT`, appended provenance to notes, and inserted a Mnemosyne `agent_logs` row.
**Output:** `_claudia/claudia.db`
**Notes:** GPCO 410 sibling rows were checked after the update and remained unchanged; Final Exam remains pending, Data Memo alternatives remain `alternate_option`, and the selected Regime Type data memo remains completed.

### 2026-05-21 - GPEC 446 Homework II deadline correction
**Requested by:** Edgar
**What was done:** Updated exactly one assignment row in `_claudia/claudia.db`: GPEC 446 — Quantitative Methods 3 `Homework II` id 12 moved from Saturday `2026-05-23 23:59` to Sunday night `2026-05-24 23:59` America/Los_Angeles. Preserved Edgar's wording in the row notes and recorded the ambiguity resolution that "midnight on Sunday" was interpreted against the existing Saturday 23:59 row.
**Output:** `_claudia/claudia.db`
**Notes:** Set `deadline_source='edgar_correction'`, `source_confidence='confirmed_by_edgar'`, `date_kind='hard'`, and `last_verified_at='2026-05-21 12:27:59 PDT'`; inserted a matching Mnemosyne `agent_logs` row.

### 2026-05-26 - Embedding Index Health Audit
**Requested by:** Edgar
**What was done:** Inspected `_claudia/claudia.db` read-only for embedding schema, vector dimensions, nulls, row counts, chunk integrity, timestamps, source-file coverage, and drift against `_claudia/embeddings.py` behavior.
**Output:** Relay-ready audit returned to Claudia; no database changes.
**Notes:** Embedding blobs are structurally healthy: 9,130 chunks, 182 source paths, all `nomic-embed-text`, all 3,072-byte 768-float blobs, no null text/blob/model fields, no duplicate or gapped chunk indices. Main drift is metadata/source hygiene: 39 embedded sources no longer exist on disk, five embedded sources are not current expected file sources, `files.indexed` has 46 false negatives plus one non-indexable false positive, and one existing indexable image PDF has no extractable text.

### 2026-05-27 - Local gcalcli calendar fallback capability
**Requested by:** Claudia
**What was done:** Inspected `_claudia/claudia.db` schema for a suitable capability/tool record pattern, then recorded the verified local `gcalcli` Google Calendar fallback as an Open Brain `brain_memories` capability row and an `agent_logs` trace row. Updated Mnemosyne context with the operational rule and caution around calendar writes.
**Output:** `_claudia/claudia.db`; `_claudia/agents/mnemosyne/AGENT_CONTEXT.md`
**Notes:** `brain_memories` id=2 records `/opt/homebrew/bin/gcalcli`, version 4.5.1, successful authenticated `gcalcli list`, visible calendars, and read/fallback usage guidance. After briefly starting Ollama, vector indexing succeeded for the new memory row using the sqlite-vec backend.

### 2026-05-27 - Email account access registry
**Requested by:** Edgar
**What was done:** Added an `email_accounts` table to `_claudia/claudia.db` and registered two mailbox access paths: UCSD Email (`eagunias@ucsd.edu`) via `_claudia/gmail_dispatch_json.py` and the local gcloud profile, and Personal Gmail (`edgar.agunias@gmail.com`) via the Codex Gmail connector.
**Output:** `_claudia/claudia.db`; `_claudia/agents/mnemosyne/AGENT_CONTEXT.md`
**Notes:** UCSD access verified on 2026-05-27 with the helper's `profile`, `search --full`, and `dispatch` commands. Personal Gmail remains connector-scoped rather than CLI-readable.

### 2026-05-27 - Daily vector DB maintenance
**Requested by:** Claudia / Edgar
**What was done:** Inspected the existing vector setup (`_claudia/embeddings.py`, `_claudia/brain.py`, `_claudia/system/open-brain.md`, vector dashboard server, SQLite schemas, and prior task logs). Ran the established course-material embedding update path after starting local Ollama, then migrated refreshed legacy embeddings into the Open Brain sqlite-vec layer and ran Open Brain vector indexing. Cleaned 109 orphaned Open Brain mirror rows whose `source_table='embeddings'` source ids no longer existed after reindexing.
**Output:** `_claudia/claudia.db`; `_claudia/agents/mnemosyne/TASK_LOG.md`
**Notes:** Final verification: `embeddings` has 9,136 chunks across 182 source paths, all embedding blobs are 3,072 bytes, `PRAGMA integrity_check` returned `ok`, and Open Brain vector status reports 9,144 total vector items/embeddings/sqlite-vec rows: 9,136 legacy embedding rows plus 3 handoffs, 3 events, and 2 memories. Existing drift remains in the legacy status metric: 182 indexed sources vs. 180 DB-indexable file rows because some embedded sources are outside the current `files` table source set.

### 2026-05-27 - Daily vector DB maintenance
**Requested by:** Claudia / Edgar
**What was done:** Re-ran the existing vector maintenance workflow for the legacy course-material embedding table and the Open Brain sqlite-vec layer. Started local Ollama after the first legacy indexing attempt reported it was unavailable; the subsequent run found no new embeddable chunks, migrated no new legacy rows, and skipped all current Open Brain rows.
**Output:** `_claudia/claudia.db`; `_claudia/agents/mnemosyne/TASK_LOG.md`
**Notes:** Final verification: `embeddings` remains 9,136 chunks across 182 source paths; Open Brain vector status remains 9,144 vector items/BLOB embeddings/sqlite-vec rows; `PRAGMA integrity_check` returned `ok`; embedding blobs remain uniformly 3,072 bytes; zero Open Brain `embeddings` mirror rows are orphaned. Changed-doc scan found several May 27 course study guides, agent memory files, dispatches, and `edgar/` outputs outside the legacy `files` table scope, so they were not ad hoc-ingested.

### 2026-05-27 — Spring 2026 Projected Grades Calculation and Report
**Requested by:** Edgar
**What was done:** Extracted all raw grades, assignment weights, and class statistics across five courses from `_claudia/claudia.db`. Audited course agent memories and syllabus policies to identify grading curves, drop rules, and attendance weights. Performed comprehensive weighted grade projections for GPCO 403, GPCO 410, GPEC 446, GPPS 444, and GPPS 463 under multiple drop/participation scenarios and relative to class means. Generated a highly polished, formatted grade projection briefing artifact with diagnostics (e.g. flagging a 0.0/1.0 attendance quiz in GPPS 463). Verified the exact SQLite query traceback for the GPEC 446 Homework I score (20.5/25.0, class mean 22.46) to ensure database transparency.
**Output:** Grade projection report artifact written to `/Users/edgar/.gemini/antigravity/brain/2761f606-5ec5-4f96-b9d2-6ec9b4e774ac/grade_projection_report.md`.
**Notes:** Highlighted strategic high-risk areas (GPPS 463 is currently 6-10% below class means with a critical attendance zero) and provided actionable tactical workback recommendations for Edgar's remaining finals and data project. Traceability checked: Homework I data resides in `grades` table row `id = 12`, referencing `course_id = 3` (GPEC 446) and `assignment_id = 10` (Homework I).

### 2026-05-28 - Daily vector DB maintenance
**Requested by:** Claudia / Edgar
**What was done:** Re-read the Claudia startup and Open Brain/vector maintenance docs, checked the legacy `embeddings` table and Open Brain vector status, started local Ollama when the documented embedding refresh reported it offline, and re-ran the established maintenance path: `python3 _claudia/embeddings.py index`, `python3 _claudia/brain.py migrate-legacy-embeddings --backend auto`, and `python3 _claudia/brain.py vector-index --backend auto`. Verified effective source-of-truth coverage against the `files` table and reading-summary overrides instead of ad hoc ingesting out-of-scope documents.
**Output:** `_claudia/agents/mnemosyne/TASK_LOG.md`
**Notes:** No new legacy chunks or Open Brain vectors were needed. Final verification stayed at 9,136 legacy embedding rows across 182 indexed sources and 9,144 Open Brain vector rows with `sqlite-vec` ready and zero orphaned `source_table='embeddings'` mirror rows; `PRAGMA integrity_check` returned `ok`; a vector smoke test for `gcalcli calendar fallback` returned the expected `brain_memories` capability row. Effective changed-source scan found zero modified registered effective sources, one registered PDF that still has no extractable text (`knowledge/obsidian/000 AI Analysis/AI Tools/AI Workflow Reconnaissance for Graduate Work in the Human Sciences 2025-2026.pdf`), and 37 registered file paths now missing on disk.

### 2026-05-28 - Emzingo internship interview background profile
**Requested by:** Claudia
**What was done:** Gathered a concise, interview-relevant profile of Edgar's background for an Emzingo internship interview using only local Claudia workspace memory, course memories, database rows, resume material, and representative coursework artifacts.
**Output:** Returned to Claudia; no content files edited.
**Notes:** Evidence supports positioning around UCSD GPS global policy training, causal inference and quantitative methods, sociology-based qualitative/mixed-methods grounding, policy memo/data brief writing, Southeast Asia/security/development interests, multilingual/multicultural experience, and student governance/service roles. Private details were intentionally minimized in the handoff.

### 2026-05-28 — GPCO 410 Midterm Grade Sync and Spring Quarter Projections
**Requested by:** Edgar
**What was done:** Updated the SQLite database `claudia.db` with Edgar's perfect midterm score of 100/100 (100.0%) for GPCO 410. Regenerated the main HTML dashboard. Recalculated GPCO 410 grade projections (rising to 95.20% raw average of graded work, projecting to a solid A) and overall Spring 2026 GPA across three performance scenarios.
**Output:** SQLite update in `_claudia/claudia.db`; updated dashboard in `_claudia/dashboard.html`; grade projection report written to `grade_projection_report.md` in the current conversation's brain folder.
**Notes:** The perfect midterm exam grade (30% weight) shifts GPCO 410 projections into the A/A- curved tier and elevates the quarter GPA projection range to 3.53 - 3.80.

### 2026-05-30 - Daily vector DB maintenance
**Requested by:** Claudia / Edgar
**What was done:** Re-discovered the existing vector setup, scanned the configured `files`/`readings` source set for changed, missing, and never-indexed effective sources, started local Ollama, and ran the established maintenance path: `python3 _claudia/embeddings.py index`, `python3 _claudia/brain.py migrate-legacy-embeddings --backend auto`, and `python3 _claudia/brain.py vector-index --backend auto`.
**Output:** `_claudia/claudia.db`; `_claudia/agents/mnemosyne/TASK_LOG.md`
**Notes:** Legacy indexer found no new embeddable chunks; the one never-indexed registered Obsidian PDF still has no extractable text. Open Brain migrated zero legacy rows and vector-indexed one pending `brain_memories` row, bringing vector status to 9,145 items/embeddings/sqlite-vec rows: 9,136 legacy embedding mirrors, 3 handoffs, 3 events, and 3 memories. Final checks: `PRAGMA integrity_check` returned `ok`, all legacy embedding blobs are 3,072 bytes, zero null legacy embedding/text/model fields, zero orphaned legacy vector mirrors, and vector smoke query for `gcalcli calendar fallback` returned the expected `brain_memories#2` capability row.
