# Hephaestus -- Task Log

| Date | Task | Files | Outcome |
|------|------|-------|---------|
| 2026-04-13 | Build shared system layer: manifest.json, system README, rewrite AGENTS.md, edit CLAUDE.md and agent-onboarding.md | `_claudia/system/manifest.json`, `_claudia/system/README.md`, `AGENTS.md`, `CLAUDE.md`, `_claudia/sop/agent-onboarding.md` | Complete -- all files created/edited, JSON valid |
| 2026-04-13 | Regenerate dashboard HTML from updated claudia.db | `_claudia/dashboard.py` -> `_claudia/dashboard.html` | Complete -- script ran with no errors |
| 2026-04-13 | Parse page counts from 5 course syllabi, populate readings.pages in DB, add Pages column to course table and total pages stat card in dashboard | `_claudia/claudia.db`, `_claudia/dashboard.py`, `_claudia/dashboard.html` | Complete -- 25 readings updated (24 from GPCO 410, 1 from GPCO 403); GPEC 446, GPPS 444, GPPS 463 had no page ranges in syllabi |
| 2026-04-13 | Count pages directly from PDFs for GPEC 446, GPPS 444, GPPS 463 readings | `_claudia/claudia.db`, `_claudia/dashboard.html` | Complete -- 29 readings updated; Mastering Metrics Ch 1-5 from TOC; TCHW all chapters from TOC; GPPS 463 all 6 readings from actual PDFs; Irregular Warfare = 1-page handout; Keegan excerpt = 33 pages; Field Experiments and Wooldridge PDFs not found in workspace (ids 20, 21, 22 still 0) |
| 2026-04-13 | Dashboard time tracker + reading speed enhancements | `_claudia/claudia.db`, `_claudia/dashboard.py`, `_claudia/dashboard.html` | Complete -- (1) created time_log table, imported 12 CSV rows; (2) computed per-course reading speeds (GPPS 463: 28 pg/hr, GPCO 410: 6 pg/hr, GPPS 444: 21 pg/hr, fallback 15 pg/hr); (3) added Est. Time column to Readings table; (4) added Weekly Reading Load stat card; (5) added Study Time Tracker collapsible with session log and per-course summary with progress bars; (6) added Speed/Est. Total Time to Per-Course Breakdown; (7) added reading load subtitle to week view |
| 2026-04-13 | Dashboard major restructure: compact header/cards, 3-tab layout, sub-tabs for Timeline | `_claudia/dashboard.py`, `_claudia/dashboard.html` | Complete -- (1) header compressed to single line; (2) stat cards tighter grid (7 across, smaller padding); (3) top-level tabs restructured to Timeline/Readings/Overview; (4) Timeline has sub-tabs: Week View / Calendar / Eisenhower Matrix; (5) Readings tab contains Readings Status + Study Time Tracker; (6) Overview tab contains Per-Course Breakdown + Embeddings + Recent Activity; (7) course tags fixed with flex-shrink:0 and white-space:nowrap throughout |
| 2026-04-13 | Fix week chevron rotation in Readings tab -- chevrons on open weeks didn't rotate back when collapsed | `_claudia/dashboard.py`, `_claudia/dashboard.html` | Complete -- removed inline style from week chevrons; CSS class rule `.collapsible-header.open .chevron` now handles rotation consistently for all weeks |
| 2026-04-13 | Collapsible week groups in Readings tab | `_claudia/dashboard.py`, `_claudia/dashboard.html` | Complete -- readings now rendered as per-week collapsible sections using existing chevron pattern; past weeks (1-2) default collapsed, current and future weeks (3+) default expanded |
| 2026-04-13 | Auto-sync time tracker CSV on Eos dispatch | `_claudia/sync_timelog.py`, `_claudia/skills/daily-briefing.md` | Complete -- created sync_timelog.py (full replace import, 13 rows); updated daily-briefing skill with Step 0 instructing Eos to run sync + dashboard regen before briefing |
| 2026-04-15 | Study Guides folder rollout: create `Study Guides/` in all 5 course folders, move 2 Ares files out of `GPPS 444/_agent/`, update CLAUDE.md directory tree and add Study Guides Convention section | 5x `[Course]/Study Guides/`, `GPPS 444/Study Guides/chevauchee_explainer.md`, `GPPS 444/Study Guides/ch5_new_weapons_new_tactics_1pager.md`, `CLAUDE.md` | Complete -- all 5 folders created idempotently, both files moved (sources gone, targets present), CLAUDE.md tree updated and new "Study Guides Convention" section inserted between Inbox Protocol and Skills Available. Convention: per-course Study Guides for single-course material; `_claudia/study_guides/` reserved for cross-class |
| 2026-04-16 | Embedding pipeline delta refresh | `_claudia/claudia.db` (embeddings table) | Complete -- delta detection worked: 117 files skipped unchanged, 20 new/modified indexed. Corpus 133 -> 144 files, 6,410 -> 7,482 chunks (+1,072). Biggest delta was QM3 with 11 files / 1,053 chunks. Flags: `Mastering 'Metrics` double-indexed in DB (two rows, same PDF path, needs Mnemosyne dedupe); 7 files uncovered (scan-only PDFs: Keegan Flesh, Breitenfeld, Diamond, Acemoglu Dutch-in-Indonesia, several GPCO 410 readings; 1 encrypted RAND 2020 needs `cryptography>=3.1`). Two pypdf "wrong pointing object" warnings on QM3 L1/L5 slides but both indexed successfully. |
| 2026-04-16 | Triton Food Pantry schedule lookup (image OCR fallback) | Chat reply to Claudia | Complete -- Gmail MCP returns plaintext only so newsletter's embedded schedule image was not extractable. Pulled canonical Spring Quarter 2026 schedule from UCSD Basic Needs website, cross-verified against Week 3 newsletter reopening language. Student Center A: Mon 11:00-7:30, Wed 9:30-6:30, Thu 1:00-7:00, Fri 5:30-7:30 (closed Tue/Sat/Sun). Graduate Housing (One Miramar): Tue 11:00-7:00, Wed 1:30-4:30, Thu 4:30-7:30, Fri 1:00-4:30, Sat 9:30-1:30 (closed Mon/Sun). Third location coming to New Marshall Buildings, hours TBA. |
| 2026-04-20 | Accept all tracked changes + strip comments from QM3 HW1 docx | `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1/HW1_Agunias.docx` | Complete -- LibreOffice unavailable on this machine, so used direct OOXML manipulation via lxml (zipfile + XML rewrite). Accepted 33 `<w:ins>` (unwrapped), removed 33 `<w:del>` blocks, handled paragraph-mark deletions by merging into next paragraph, stripped 31 comment ranges/references and dropped `word/comments*.xml` + `word/people.xml` parts plus their Content_Types Overrides and document.xml.rels Relationships. Also stripped `rPrChange`/`pPrChange`/etc. revision metadata. Verified: zero residual ins/del/delText/commentRangeStart/commentReference markers, python-docx opens cleanly, 253 paragraphs / 2 tables / 2 image relationships preserved. Originals `HW1_Agunias_ORIGINAL.docx` and `HW1_Agunias_TRACKED.docx` left intact. |
| 2026-04-16 (night) | Dashboard April calendar rendering bug: only 4 columns visible | `_claudia/dashboard.html` line 178 | Complete -- root cause was `grid-template-columns: repeat(7, 1fr)` on `.cal-grid` where `1fr` = `minmax(auto, 1fr)` treats intrinsic min-content as a width floor. `.cal-event` children have `white-space: nowrap`, so long event titles ballooned columns 2-4 to 400-500px each, consuming the 1400px container and pushing Thu/Fri/Sat past x=1457 where `overflow: hidden` (for corner-cell border-radius clipping) silently hid them. Fix: `repeat(7, minmax(0, 1fr))` drops the intrinsic-min-content floor. Long titles now clip via the existing `text-overflow: ellipsis` on line 197. Verified headless Chrome 1440x900 across April 2026, May 2026, March 2027, June 2027 - all 7 tracks render at exactly 199px. Pattern for future CSS-Grid work on layouts with nowrap text children: `minmax(0, 1fr)` is the correct default; plain `1fr` is a footgun. |

### 2026-04-19 — GPEC 446 Homework 1 build - stream idle timeout
**Requested by:** Claudia (after Tyche stalled twice)
**What was done:** Dispatched on opus to build QM3 Homework 1 end-to-end: write hw1_build.R, iterate until it runs clean, wrap in HW1_Agunias.Rmd, knit HTML, convert to PDF via Chrome headless. Explicit guidance to avoid Read on the 44MB atlas.csv. Ran ~9 minutes across 12 tool calls, then stream idle timeout with nothing written to disk.
**Output:** none - `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1/` still contains only the instructions docx and raw CSV.
**Notes:** Failure was not CSV-read-related; likely long silent compute windows (R package install, read.csv on 44MB, rmarkdown::render, Chrome print) stacked past the 600s watchdog. Going forward, split this class of build into sub-three-minute phases and drive execution from the main conversation between phases rather than inside one subagent session. Full pattern captured in `project_subagent_stream_timeouts_2026-04-19.md` in Claudia memory.

### 2026-04-20 — Accept All Track Changes on HW1 docx
**Requested by:** Claudia (on Edgar's instruction)
**What was done:** Accepted all 33 tracked insertions and removed all 33 deletions in `HW1_Agunias_TRACKED.docx`, stripped 31 comment ranges/references, dropped `word/comments*.xml` and `word/people.xml` parts plus their `[Content_Types].xml` Overrides and `document.xml.rels` Relationships, removed revision-metadata nodes (`rPrChange`, `pPrChange`). Wrote the clean result as canonical `HW1_Agunias.docx`. Used direct OOXML manipulation via `lxml` + `zipfile` since LibreOffice is not installed on this machine — the docx skill's `accept_changes.py` recipe depends on LO.
**Output:** `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1/HW1_Agunias.docx` (clean canonical).
**Notes:** Verified 0 `w:ins`, 0 `w:del`, 0 `w:delText`, 0 `w:commentRangeStart`, 0 `w:commentReference` residuals. 253 paragraphs, 2 tables, 2 image relationships preserved. Stored the lxml + zipfile script pattern for future track-accept jobs on this machine.

### 2026-04-23 — Calendar timeblocking for Thu/Fri work push
**Requested by:** Claudia (on Edgar's instruction)
**What was done:** (1) Created 6 timeblock events on Edgar's primary calendar covering Thu/Fri HW1 + Orange Memo + Polity work; returned event IDs. (2) After Edgar clarified that study/coursework blocks belong on the Learning calendar (ID `dicjpk2av0g6nkujknnesgu8fs@group.calendar.google.com`), moved all 6 via delete-and-recreate (Google Calendar MCP exposes no native move). Flagged that recreated titles persisted emdashes/en-dashes. (3) Updated 5 Learning-calendar titles to strip emdashes and en-dashes per standing style rule. (4) Attempted to create 3 additional reading blocks on Learning calendar, but Google Calendar MCP tools were not in this run's tool context; Claudia created them directly.
**Output:** 6 timeblocks (now on Learning calendar, dash-free titles) + 3 reading blocks created by Claudia.
**Notes:** Three lessons logged to FEEDBACK: (a) study/coursework blocks default to Learning calendar, never primary; (b) emdash/en-dash style rule extends to calendar event summaries, MCP does no filtering; (c) per-run tool availability varies for this agent, verify tool context before committing to a plan that depends on a specific MCP.

### 2026-04-27 — GPEC 446 Homework 1 Codex R cleanup and compiled answers
**Requested by:** Edgar
**What was done:** Updated the Codex copy of `Homework_1_Codex.R` to save all generated tables and figures to disk, including the Q4 OVB table, Q7-Q9 fixed-effects table, open-question table, IV table, and code-understanding glossary. Then created a compiled Markdown answer document with bracketed artifact labels for tables and images.
**Output:** `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1 - codex/Homework_1_Codex.R`, `README.md`, `Homework_1_Answers_Compiled.md`, plus generated HTML/PNG artifacts.
**Notes:** `Rscript Homework_1_Codex.R` runs successfully. Important statistical note preserved in the compiled answers: in the interaction model, the `-0.442` poverty coefficient is the majority-white slope; the majority-non-white implied slope is `-0.442 + 0.306 = -0.136`.

### 2026-04-27 — Codex transition hardening for Claudia
**Requested by:** Edgar
**What was done:** Added a Codex-first workflow document, created a neutral `_claudia/agent_definitions/` mirror for all 11 agent definitions, updated the manifest to prefer neutral definitions with `.claude/agents` as legacy fallback, and patched startup docs, onboarding SOPs, disclosure templates, and key skills to remove execution-breaking Claude-only assumptions.
**Output:** `_claudia/system/CODEX_WORKFLOW.md`, `_claudia/agent_definitions/*.md`, `AGENTS.md`, `CLAUDE.md`, `_claudia/system/manifest.json`, `_claudia/system/README.md`, `_claudia/sop/*`, selected `_claudia/skills/*`, `.claude/agents/hermes.md`, `.claude/agents/calliope.md`.
**Notes:** Verified `manifest.json` is valid JSON, all manifest `definition`, `definition_legacy`, and `memory` paths resolve, canonical and legacy agent-definition directories match, and the GPEC 446 Codex R workflow runs with `Rscript` exit code 0.

### 2026-04-27 — Dashboard Week 5 state update
**Requested by:** Claudia
**What was done:** Updated `_claudia/dashboard.html` from Week 3 to Week 5 for the visible dashboard subtitle, current-week reading-load card, and JavaScript `CURRENT_WEEK` state. Collapsed Week 3 and Week 4 reading sections so Week 5 remains the active open week.
**Output:** `_claudia/dashboard.html`
**Notes:** Preserved existing dirty worktree changes and did not regenerate the dashboard.

### 2026-04-27 — Save workflow commit and push rule
**Requested by:** Edgar
**What was done:** Updated the Claude `/save` command and Codex Save Protocol so future saves commit and push only the scoped saved changes, with explicit staging, meaningful commit messages, current-branch push, and failure reporting. Also aligned the `/save` confirmation section with the current output-disclosure SOP.
**Output:** `.claude/commands/save.md`, `_claudia/system/CODEX_WORKFLOW.md`, `CLAUDE.md`, `_claudia/agents/hephaestus/TASK_LOG.md`
**Notes:** Did not run `git commit` or `git push` because the worktree already contains many unrelated dirty changes and this task was to update the command definition safely.

### 2026-04-27 — Edgar temporary output landing zone
**Requested by:** Edgar
**What was done:** Created the repo-root `edgar/` folder with a lightweight README and updated central workflow docs so agents can place Edgar-facing day-scoped summaries there when Edgar asks for a collect-first workflow. Documented that durable course copies can later be sorted into course Study Guides and that existing course-folder summaries should not be moved without instruction.
**Output:** `edgar/README.md`, `CLAUDE.md`, `_claudia/system/CODEX_WORKFLOW.md`
**Notes:** Searched for Apr 27 summary files by date/name and found none to move.

### 2026-04-27 — Vendor-neutral Claudia orchestrator migration
**Requested by:** Claudia (on Edgar's instruction)
**What was done:** Created `_claudia/system/CLAUDIA.md` as the canonical vendor-neutral orchestrator map, replaced `CLAUDE.md` with a deprecated compatibility pointer, and updated startup/workflow/manifest references away from `CLAUDE.md`. Documented `.claude/agents/` as a deprecated compatibility mirror rather than the source of truth.
**Output:** `_claudia/system/CLAUDIA.md`, `CLAUDE.md`, `AGENTS.md`, `_claudia/system/CODEX_WORKFLOW.md`, `_claudia/system/manifest.json`, `_claudia/system/README.md`, `_claudia/sop/agent-onboarding.md`, `_claudia/agent_definitions/hermes.md`, `_claudia/memory/preferences.md`
**Notes:** Verified `manifest.json` parses. Did not delete `.claude/` mirrors because current consumers may still rely on them.

### 2026-04-27 - Codex-only Claude Code support cleanup
**Requested by:** Edgar
**What was done:** Removed the scoped Claude Code support surfaces and updated active Claudia docs so agent definitions are Codex-only through `_claudia/agent_definitions/`. Removed `definition_legacy` and legacy agent-definition directory metadata from the manifest while keeping `CLAUDE.md` as a deprecated pointer.
**Output:** Deleted `.claude/.DS_Store`, `.claude/settings.local.json`, `.claude/commands/save.md`, and `.claude/agents/`; updated `AGENTS.md`, `_claudia/system/CLAUDIA.md`, `_claudia/system/CODEX_WORKFLOW.md`, `_claudia/system/README.md`, `_claudia/system/manifest.json`, `_claudia/sop/agent-onboarding.md`, and `_claudia/agent_definitions/hermes.md`.
**Notes:** Assignment artifacts in `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1 - claude/` were intentionally left untouched. `CLAUDE.md` remains as the deprecated legacy pointer.
### 2026-04-28 — Dashboard Deadline Field Support
**Requested by:** Claudia / Edgar
**What was done:** Updated `_claudia/dashboard.py` to derive the current academic week from the local date, read optional normalized assignment deadline fields, serialize due times/source metadata to the dashboard, use local browser dates for today highlighting, and use due time when computing matrix urgency. Regenerated `_claudia/dashboard.html`.
**Output:** `_claudia/dashboard.py`; `_claudia/dashboard.html`
**Notes:** Dashboard code is backward-compatible when normalized columns are absent. Past-week assignments are no longer auto-marked completed in the UI; status must come from the DB.

### 2026-04-28 — Dashboard Regenerated After Syllabus Normalization
**Requested by:** Claudia
**What was done:** Regenerated `_claudia/dashboard.html` after Mnemosyne's syllabus-extraction normalization pass added structured due times and missing discussion-post rows.
**Output:** `_claudia/dashboard.html`
**Notes:** Verification query shows Apr 28/29 deadlines and May 4/5 exams with structured due times.

### 2026-04-29 — Bureaucratic Boredom Index R Project Paused
**Requested by:** Claudia / Edgar
**What was done:** Created `democracy_as_boredom_bbi/` with R project structure, acquisition/cleaning/dictionary/scoring/visualization/modeling/validation scripts, README, methods/limitations/next-steps memos, and an R Markdown report shell. Ran the pipeline far enough to scrape and score 309 APP speeches, generate figures, and generate preliminary model/summary tables. Fixed scraper selectors for future reruns, but Edgar paused during the rerun before final validation.
**Output:** `democracy_as_boredom_bbi/` project folder with raw, clean, scored, figure, table, script, doc, and log files.
**Notes:** Current generated CSV/table/figure outputs should be treated as partial because they were produced before the president metadata selector fix and have `president` missing. Resume by rerunning `Rscript scripts/00_run_pipeline.R` from `democracy_as_boredom_bbi/`, then verify validation outputs and render `docs/bbi_report.Rmd`.

### 2026-04-29 — Bureaucratic Boredom Index R Project Completed
**Requested by:** Claudia / Edgar
**What was done:** Resumed the BBI checkpoint, reran `Rscript scripts/00_run_pipeline.R` successfully, verified raw/clean/scored row counts and president metadata, rendered `docs/bbi_report.html`, and removed incidental `.DS_Store` files from the project folder.
**Output:** `democracy_as_boredom_bbi/data_raw/presidential_speeches_raw.csv`, `data_clean/presidential_speeches_clean.csv`, `data_clean/presidential_speeches_bbi_scored.csv`, `outputs/figures/`, `outputs/tables/`, `docs/validation_memo.md`, `docs/bbi_report.html`.
**Notes:** Final run contains 309 APP speeches, 63 inaugural and 246 State of the Union/written message items, with president populated in raw, clean, and scored outputs. Remaining limitations: U.S.-only pilot, no party/divided-government/crisis/war metadata, dictionary scores require close-reading validation.

### 2026-04-29 — BBI Metadata Enrichment and ASR-Style Manuscript
**Requested by:** Edgar
**What was done:** Added `scripts/02b_enrich_metadata.R` and wired it into the BBI pipeline. Enriched raw, clean, and scored data with presidential party, Congress control/divided government, major-war period, recession indicator, GDP, and crisis-period fields; reran scoring, figures, validation, and regression tables. Updated project docs/report and exported refreshed HTML/PDF. Drafted an ASR-style manuscript after inspecting the ASR sample article in `inbox/`.
**Output:** `democracy_as_boredom_bbi/data_clean/presidential_speeches_bbi_scored.csv`, `logs/metadata_enrichment_log.md`, `outputs/tables/preliminary_models_tidy.csv`, `docs/bbi_report.html`, `docs/bbi_report.pdf`, `docs/bbi_asr_style_manuscript.md`, `.html`, `.pdf`, `.docx`.
**Notes:** Metadata coverage after enrichment: party 309/309, Congress status 309/309, major-war flag 309/309, recession 226/309, GDP 110/309. Model 3 now includes divided government, major war, recession, and speech type. GDP begins in 1947 and remains for later postwar models rather than the main long-series regression.
### 2026-05-02 - Course-Local Artifact Archive Implementation
**Requested by:** Edgar
**What was done:** Implemented the course-local archive convention for obvious superseded version families across course folders; added archive SOP and index; updated agent contexts with the new protocol.
**Output:** [Course Folder]/.archive/, `_claudia/sop/artifact-archive.md`, `_claudia/sop/iterative-file-naming.md`, agent `AGENT_CONTEXT.md` files
**Notes:** Keep current candidates visible, move superseded generated iterations to `[Course Folder]/.archive/<project_slug>/`, and update `[Course Folder]/.archive/ARCHIVE_INDEX.md`.

### 2026-05-03 - GPCO 403 midterm reference enlarged-visual build
**Requested by:** Claudia / Edgar
**What was done:** Updated the GPCO 403 ReportLab builder from v1.4.1 to v1.4.2 so the small main-page visual slot becomes a pointer and each theory page is followed by an enlarged visual page. Ran syntax, build, PDF metadata, outline/text, image-object, and rendered-page checks.
**Output:** `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPCO 403 - Intl Econ - Handley/Study Guides/build_midterm_theory_reference.py`; `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.4.2.pdf`; `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.4.2_notes.md`.
**Notes:** Removed incidental `Study Guides/__pycache__/` after `py_compile`; no staging or commit performed.

### 2026-05-18 - GPEC 446 Homework 2 Part II RDD implementation
**Requested by:** Edgar via Claudia/Tyche
**What was done:** Created a reproducible Part II R script for the Maimonides Rule RDD, inspected `grade5.dta`, generated the enrollment histogram and cutoff plots, estimated manual local-linear discontinuities, installed and ran `rdrobust` in a project-local output library, and ran a disadvantaged-covariate smoothness falsification test.
**Output:** `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez/Assignments/Homework 2/Homework_2_Part_II_rdd.R`; `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez/Assignments/Homework 2/PART_II_NOTES.md`; `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez/Assignments/Homework 2/outputs/part_ii/`
**Notes:** Stayed inside the Part II write scope and did not edit Part I or the combined report. `rdrobust` emitted mass-point warnings because `school_enrollment` is integer-valued; this is flagged for Tyche's interpretation.

### 2026-05-03 - GPCO 410 Midterm Flashcard HTML
**Requested by:** Claudia / Edgar
**What was done:** Created a standalone direct-open HTML/CSS/JS flashcard drill tool for the 11 GPCO 410 midterm theory entries. Fronts show theory title plus smaller italic author/source line; backs give 2-3 sentence exam-useful essences.
**Output:** `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPCO 410 - Intl Pol:Sec - Praether/Study Guides/gpco410_midterm_flashcards.html`
**Notes:** Verified the file exists and contains 11 title, author, and essence records, plus keyboard controls and internal output disclosure.

### 2026-05-04 - Graduate Student Lounge GPSA PPTX
**Requested by:** Claudia
**What was done:** Created a 10-slide GPSA briefing deck for the Graduate Student Lounge using the standard PowerPoint template, the committee meeting notes, and two selected lounge photos.
**Output:** `inbox/GLO/Graduate_Student_Lounge_GPSA_v1.0.0_working.pptx`
**Notes:** Verified with MarkItDown extraction, placeholder/legacy-text scan, PowerPoint PDF render/contact-sheet visual check, final Quick Look thumbnail, and pptx geometry checks. The second PowerPoint export pass hung after a minor slide 9 geometry trim and was stopped; final text/geometry checks passed afterward.

### 2026-05-04 - Dashboard Refresh
**Requested by:** Claudia
**What was done:** Regenerated `_claudia/dashboard.html` from the current `_claudia/claudia.db` using the existing dashboard generator.
**Output:** `_claudia/dashboard.html`
**Notes:** Verified local date banner, Week 6 state, headline cards, and assignment/readings/file/embedding counts against direct SQLite queries.

### 2026-05-04 - Dashboard Refresh After GPCO 410 Midterm Completion
**Requested by:** Claudia
**What was done:** Regenerated `_claudia/dashboard.html` from the current `_claudia/claudia.db` after Mnemosyne marked the GPCO 410 midterm completed.
**Output:** `_claudia/dashboard.html`
**Notes:** Verified the embedded assignment JSON now has GPCO 410 Midterm Exam id 18 as `completed` with submitted timestamp `2026-05-04 19:50:54 PDT`; headline assignment card now reads 34 total, 21 up, 13 done.

### 2026-05-05 - Delegation and Orchestrator Hardening
**Requested by:** Claudia / Edgar
**What was done:** Tightened Claudia startup and delegation rules, added the delegation gate SOP, registered it in the SOP index and manifest, required startup reads of `_claudia/memory/preferences.md`, and added a compact manifest routing surface.
**Output:** `AGENTS.md`, `_claudia/system/CLAUDIA.md`, `_claudia/system/CODEX_WORKFLOW.md`, `_claudia/system/manifest.json`, `_claudia/sop/README.md`, `_claudia/sop/delegation.md`
**Notes:** Local fallback now must be explicitly declared before work and logged to the owning agent's memory before final handoff.

### 2026-05-05 - Live Dashboard Server
**Requested by:** Claudia / Edgar
**What was done:** Added a local live dashboard server with `/api/dashboard`, `/api/health`, and `/events` SSE endpoints; kept static dashboard generation intact; added optional filesystem notification for `_claudia/claudia.db` plus WAL/SHM sidecars with a slow fallback check; added browser-side SSE refresh and a dark/aged-paper theme toggle.
**Output:** `_claudia/dashboard.py`; `_claudia/dashboard_server.py`; `_claudia/dashboard.html`
**Notes:** Verified with Python compile, static generation, curl health/API/HTML checks, and an SSE filesystem-change smoke test from `http://127.0.0.1:8765`.

### 2026-05-05 - Dashboard Redesign Concept Mockups
**Requested by:** Edgar
**What was done:** Created three static review mockups for the Claudia dashboard redesign without replacing the current dashboard. Concepts emphasize due-today, next 48 hours, and course workload/status with Apple-like, EPA field binder, and hybrid operational directions.
**Output:** `_claudia/design_concepts/dashboard_redesign_2026-05-05/`
**Notes:** Used live `/api/dashboard` data where available. Current dashboard generator/server files were not edited.

### 2026-05-05 - Dashboard Redesign Concept Mockups v2 With Screenshot References
**Requested by:** Claudia / Edgar
**What was done:** Reran the Claudia dashboard redesign concepts using the attached dashboard and EPA Graphic Standards screenshots as visual references. Created three revised static HTML concepts plus rendered screenshots, emphasizing due-today, next 48 hours, course workload/status, EPA-style program colors, geometric signal patterns, sparse metadata, and strong black typography.
**Output:** `_claudia/design_concepts/dashboard_redesign_2026-05-05_v2/`
**Notes:** Did not replace the live dashboard. Used live `/api/dashboard` data for counts and next-deadline anchors. Verified rendered screenshots with Chrome headless.

### 2026-05-05 - Standards Sheet Concept Annotation Pass
**Requested by:** Edgar
**What was done:** Updated v2 dashboard concept 2 from browser annotations: removed the repeated vertical Claudia identifier clutter, replaced EPA-style program labels with course codes, and made course cards open an animated three-panel course pamphlet for readings, assignments, and exams.
**Output:** `_claudia/design_concepts/dashboard_redesign_2026-05-05_v2/concept_2_standards_sheet.html`; refreshed screenshots in `_claudia/design_concepts/dashboard_redesign_2026-05-05_v2/screenshots/`
**Notes:** Did not replace the live dashboard. Verified HTML parsing, label cleanup, accessibility hooks, and Chrome headless renders for the closed sheet and open GPCO 403 pamphlet.

### 2026-05-05 - Live Dashboard Standards Sheet Implementation
**Requested by:** Claudia / Edgar
**What was done:** Replaced the generated/live dashboard surface with the concept 2 standards-sheet design while preserving DB-backed generation, `/api/dashboard`, `/api/health`, and `/events` SSE refresh. Course cards now open a three-panel pamphlet from live payload data; completed/submitted/done records are muted, struck through, and sorted below active records.
**Output:** `_claudia/dashboard.py`; `_claudia/dashboard.html`; `_claudia/dashboard_server.py`; `_claudia/dashboard_screenshots/live_dashboard_standards_sheet_2026-05-05.png`; `_claudia/dashboard_screenshots/live_dashboard_gpco410_pamphlet_2026-05-05.png`
**Notes:** Verified Python compile, static generation, health/API/HTML/SSE curl checks, and Chrome headless screenshots. GPCO 410 payload shows Blue Memo completed and Orange Memo submitted; active memo/exam records render above completed records in the pamphlet.

### 2026-05-06 - Dashboard Daily Dispatch Integration
**Requested by:** Edgar
**What was done:** Added daily briefing discovery/parsing to `_claudia/dashboard.py`, then narrowed the dashboard surface to a compact Dispatch Signals panel so it supplements the dashboard instead of duplicating action items. The panel now extracts Weather, Personal Gmail, UCSD Email, and Delegation Suggestions.
**Output:** `_claudia/dashboard.py`; `_claudia/dashboard.html`
**Notes:** Ran `python3 _claudia/dashboard.py`; payload verification shows `today=2026-05-06`, latest dispatch `2026-05-06`, freshness `current` / `today`, and all four signal sections present.

### 2026-05-07 - Dashboard Refresh and Local Launch
**Requested by:** Edgar
**What was done:** Regenerated `_claudia/dashboard.html` from `_claudia/claudia.db` with the established dashboard generator and launched the local live dashboard server.
**Output:** `_claudia/dashboard.html`; local server at `http://127.0.0.1:8765`
**Notes:** Verified `/api/health`, `/api/dashboard`, and `/dashboard.html` with curl. Payload reports `today=2026-05-07`, Week 6, 34 assignments, 17 upcoming, 17 completed. Latest dispatch is `2026-05-07` and marked current/today.

### 2026-05-07 - Non-Blocking Subagent Dispatch Rule
**Requested by:** Edgar
**What was done:** Added Edgar's non-blocking dispatch rule to Claudia's durable preferences, Codex workflow, and delegation SOP. The rule makes dispatch-and-return the default and restricts `wait_agent` to explicit wait requests or hard parent-action dependencies.
**Output:** `_claudia/memory/preferences.md`; `_claudia/system/CODEX_WORKFLOW.md`; `_claudia/sop/delegation.md`
**Notes:** Keep Claudia available after launching workers; relay subagent handoffs as notifications arrive.

### 2026-05-07 - Save/Publish Verification Audit
**Requested by:** Claudia
**What was done:** Verified the just-created save/publish operation after commit `7ec6bee Save Claudia workspace updates` and checked remaining untracked cache folders.
**Output:** returned to Claudia
**Notes:** `HEAD` and `origin/main` both resolved to `7ec6beef4fff38f95eb296ac53d3fc4dbb317cd4`, confirming the push completed. Remaining `__pycache__` folders are untracked and not ignored by current rules; treat them as transient cleanup candidates, not save-blocking durable artifacts.

### 2026-05-09 - Diplogame How-to-Play Markdown Scaffold
**Requested by:** Claudia
**What was done:** Created an initial operational Markdown guide for the Diplogame Iran-style game pack, covering player quick-start, objectives, roles, turn flow, action/message mechanics, negotiation, scoring, Control setup, adjudication, injects, escalation, endgame, and checklists. No PDF was generated.
**Output:** `/Users/edgar/Documents/01 Projects/Diplogame/iran-style-game-pack/how-to-play.md`
**Notes:** Based on the existing Diplogame root README, pack README, player handbook, facilitator guide, setup checklist, public briefing, control references, forms, variant pack notes, web README, and ops README. Left unrelated Diplogame `.DS_Store` dirty work untouched.

### 2026-05-10 - Theory image generation SOP and skill update
**Requested by:** Claudia (for Edgar)
**What was done:** Added the approved MacIntyre prototype visual standard as a durable SOP and updated the theory-reference-pdf workflow so every reading/theory/framework requires one explanatory image plus a short mechanism/assumption/strength-limit caption.
**Output:** `_claudia/sop/theory-image-generation.md`; `_claudia/skills/theory-reference-pdf.md`; SOP registrations in `_claudia/sop/README.md`, `_claudia/system/CLAUDIA.md`, and `_claudia/system/manifest.json`
**Notes:** Project-bound generated images must be copied into course Study Guides asset folders. New image families should prototype one image for Edgar critique before batch generation.

### 2026-05-10 - GPPS 463 Midterm 2 theory reference visual-page build
**Requested by:** Claudia
**What was done:** Updated the GPPS 463 Midterm 2 ReportLab builder to insert one paired explanatory visual page after each numbered theory/framework section, using the matching workspace PNG and a concise mechanism, key-assumption, and strength/limit caption. Regenerated the PDF and verified page count, outlines, TOC annotations, embedded image XObjects, and caption text extraction.
**Output:** `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPPS 463 - Pol SEA - Ravanilla/Study Guides/build_midterm_2_theory_reference.py`; `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_2_Theory_Reference_v1.0.0.pdf`
**Notes:** PDF increased from 25 to 35 pages, with 10 visual-page bookmarks and 10 embedded image XObjects. Existing image assets were referenced in place and not overwritten.

### 2026-05-11 - Obsidian daily dispatch generator
**Requested by:** Claudia / Edgar
**What was done:** Added a plain Markdown daily-dispatch generator so Eos can produce an Obsidian-ready daily view from `_claudia/claudia.db` without running the local HTML dashboard server. The generator groups each course into due today, rest of week, and peek next week, using Obsidian task checkboxes, bold task titles, emoji markers, multi-line task blocks, and ASCII progress bars.
**Output:** `_claudia/daily_dispatch_md.py`; `_claudia/dispatches/2026-05-10_daily-dispatch.md`; `_claudia/dispatches/2026-05-11_daily-dispatch.md`; `_claudia/skills/daily-briefing.md`
**Notes:** Verified with `python3 -m py_compile _claudia/daily_dispatch_md.py` and generated May 10 and May 11 dispatch files. Calendar, weather, and email sections accept optional JSON/text inputs and degrade to clear unavailable notes when live signals are not supplied.

### 2026-05-12 - Markdown dispatch email diagnostics
**Requested by:** Claudia / Edgar
**What was done:** Added `_claudia/gmail_dispatch_json.py` and `--auto-email` support in `_claudia/daily_dispatch_md.py` so the Obsidian dispatch can collect local UCSD Gmail items or surface the exact credential failure. Fixed the helper environment handling so `gcloud` remains on PATH while using the separate `CLOUDSDK_CONFIG`.
**Output:** `_claudia/gmail_dispatch_json.py`; `_claudia/daily_dispatch_md.py`; `_claudia/dispatches/2026-05-12_daily-dispatch.md`
**Notes:** Verification showed the UCSD Gmail token is expired/revoked (`invalid_grant`) and needs browser re-auth. Personal Gmail remains Codex connector-only; the connector is live, and current personal INBOX count is zero even though unread All Mail has recent Capital One messages.

### 2026-05-14 - UCSD Gmail Re-auth Diagnostic Command Fix
**Requested by:** Claudia / Edgar
**What was done:** Confirmed the UCSD Gmail dispatch failure is a revoked/expired local gcloud ADC refresh token, then patched the Gmail dispatch helper so recovery diagnostics include the saved OAuth client file and the required `cloud-platform` plus `gmail.readonly` scopes.
**Output:** `_claudia/gmail_dispatch_json.py`
**Notes:** `python3 -m py_compile _claudia/gmail_dispatch_json.py _claudia/daily_dispatch_md.py` passed. The corrected browser OAuth flow opened successfully, but the token is not refreshed until Edgar completes the Google consent page.

### 2026-05-14 - Actual Finance SQLite cleanup
**Requested by:** Edgar
**What was done:** Backed up `2026-05-14-My Finances/db.sqlite`, added granular Actual Budget category groups/categories, recategorized obvious payee spending, converted exact matched internal money movement into native transfer pairs, and tombstoned duplicate imported transfer artifacts where an equivalent native transfer already existed.
**Output:** `2026-05-14-My Finances/db.sqlite`; backup at `2026-05-14-My Finances/backups/db.sqlite.before-finance-cleanup-20260514-233531.sqlite`
**Notes:** SQLite integrity check passes. Uncategorized non-transfer rows dropped from 139 to 1, linked transfer rows increased from 16 to 74, and transfer-link verification reports zero broken pairs. One old $25 Quicksilver Secured `Capital One Credit Card` credit was left uncategorized because it lacked a confident matching outflow.

### 2026-05-15 - Finance HTML Dashboard and SimpleFIN Sync Scaffold
**Requested by:** Edgar
**What was done:** Built a local Python-served finance dashboard around `My-Finances-cleaned-actual-export-v3/db.sqlite`, including summary cards, account balances, monthly cash flow, top spending, budget watch, recent transactions, and a server-side SimpleFIN sync endpoint. Kept SimpleFIN credentials out of browser code by reading `.env.local` on the server.
**Output:** `My-Finances-cleaned-actual-export-v3/server.py`; `simplefin_sync.py`; `dashboard.html`; `static/dashboard.css`; `static/dashboard.js`; `.env.example`; `.gitignore`; `README.md`
**Notes:** Verified `python3 -m py_compile server.py simplefin_sync.py`, `GET /api/summary`, static asset serving, and `HEAD /`. The dashboard runs at `http://127.0.0.1:8787`; sync makes a timestamped SQLite backup before writing.

### 2026-05-15 - Finance Macro Group Dashboard and Deterministic Transfer Rules
**Requested by:** Edgar
**What was done:** Reworked the dashboard to show macro spending groups first, then drill into subcategories and transactions. Added deterministic transfer-rule logic and wired sync to run those rules after importing so paired transfers are linked without AI judgment.
**Output:** `My-Finances-cleaned-actual-export-v3/server.py`; `finance_rules.py`; `simplefin_sync.py`; `dashboard.html`; `static/dashboard.js`; `static/dashboard.css`
**Notes:** Verified May 2026 macro group total equals monthly non-transfer outflow (`$1,992.17`) and current-month uncategorized transaction count is zero after labeling linked transfers as `Transfer`. SimpleFIN sync still fails because the provided setup token returns `HTTP 403 Forbidden`.

### 2026-05-15 - Finance Dashboard Interaction Polish
**Requested by:** Edgar
**What was done:** Added Percent Mode for hiding raw dollar figures, account click-through into full account transaction ledgers, Budget Watch rows that match dashboard macro groups, expandable budget subcategories, and budget usage shown as percent plus spent/budget fraction. Clarified SimpleFIN app-token handling so one-time app tokens are claimed server-side and replaced with a reusable access URL when the claim succeeds.
**Output:** `My-Finances-cleaned-actual-export-v3/server.py`; `simplefin_sync.py`; `README.md`; `static/dashboard.js`; `static/dashboard.css`
**Notes:** Manual SimpleFIN debugging showed the app token was valid and the SimpleFIN app entry became Active, but the manual claim consumed the one-time token before the reusable access URL was saved to `.env.local`. A fresh app token is needed for the patched claim-and-save path.

### 2026-05-19 - GPSA Budget Flow HTML
**Requested by:** Claudia / Edgar
**What was done:** Built a standalone interactive HTML budget-flow visualization from `inbox/GPSA 2026_2027_Draft.xlsx`, comparing 2025-2026 budget lines to the 2026-2027 proposed budget with Sankey-style flows, filters, year toggles, and a reallocation ledger.
**Output:** `edgar/gpsa_budget_flow.html`
**Notes:** Source workbook's proposed-budget summary legend contains broken `#REF!` formulas, so the artifact uses concrete line-item rows and cached totals from the workbook.

### 2026-05-19 - Budget Flow Visualization Skill
**Requested by:** Edgar
**What was done:** Captured the GPSA budget-flow design and implementation lessons as a reusable Claudia workspace skill, including workbook extraction, Sankey interactions, smooth compare animation, stable no-snap layout, upstream focus tracing, reallocation cards, and verification rules.
**Output:** `_claudia/skills/budget-flow-visualization.md`; `_claudia/system/manifest.json`
**Notes:** Use this skill for future budget-workbook requests that ask to visualize reallocations, follow the money, animate year-over-year changes, or create Monarch-style flow charts.

### 2026-05-19 - Spring Formal and GO GPS Budget Flow HTML
**Requested by:** Edgar
**What was done:** Built two standalone interactive HTML budget-flow visualizations from the Spring Fling/Formal 2026 and GO GPS Finance 2025-26 workbooks, with hard-coded extracted data, scenario toggles, Sankey flows, line-item mode, compare animation, reallocation cards, and source caveats where workbook formulas materially affected interpretation.
**Output:** `edgar/spring_fling_formal_2026_budget_flow.html`; `edgar/go_gps_finance_2025_26_budget_flow.html`; `_claudia/scripts/build_budget_flow_visualizations.py`
**Notes:** Verified cached/formula views through dependency-free XLSX XML extraction, JavaScriptCore parse checks, and headless Chrome/Selenium render plus interaction smoke tests. GO GPS source summary formula D19 omits some entered actuals and uses the budgeted Spring Fling cell, so the artifact uses concrete line rows instead.

### 2026-05-21 - UCSD Gmail helper SSL certificate fix
**Requested by:** Edgar
**What was done:** Patched `_claudia/gmail_dispatch_json.py` so Gmail API requests use certifi's CA bundle when certifi is installed, avoiding the local Python SSL issuer failure without requiring `SSL_CERT_FILE`.
**Output:** `_claudia/gmail_dispatch_json.py`
**Notes:** Verified `python3 _claudia/gmail_dispatch_json.py` succeeds without SSL environment setup and reads `eagunias@ucsd.edu` with 8 matching unread inbox messages.

### 2026-05-21 - GO GPS inventory management TEST workbook MVP
**Requested by:** Edgar
**What was done:** Built a native Excel MVP for GO GPS office and club inventory, seeded from the 2025-2026 club leadership workbook in `inbox/`. Added a pastel dashboard with KPI cards, native charts for club/category/value/consumables, cost and consumable tracking fields, dropdown-backed inventory fields, checkout/return logging, barcode intake staging, and a club directory.
**Output:** `edgar/TEST - GO GPS Inventory Management MVP.xlsx`
**Notes:** Verified the final workbook from the `edgar/` copy with formula-error scan reporting zero matches. Google Drive native Sheet creation was blocked by connector upload/create permissions, so the deliverable was placed locally as requested.

### 2026-05-21 - GO GPS inventory automation and barcode intake scaffold
**Requested by:** Edgar
**What was done:** Added workbook conditional formatting for consumable levels and quantity-available warnings, then created a Google Sheets Apps Script scaffold for stable `GOGPS-0001` Item ID generation, row formula installation, date stamping, conditional-format setup, barcode lookup, and a phone-facing scan/edit/add web-app flow.
**Output:** `edgar/TEST - GO GPS Inventory Management MVP.xlsx`; `edgar/GO_GPS_inventory_google_sheets_automation.gs`; `edgar/GO_GPS_inventory_barcode_webapp_Index.html`
**Notes:** Verified the rebuilt workbook from the `edgar/` copy with zero formula-error matches and confirmed Apps Script syntax with Node's CommonJS parser. The phone web app uses browser barcode detection where available and falls back to manual barcode entry; AppSheet remains the lower-maintenance production option for mobile barcode scanning.

### 2026-05-24 - GPSA Budget Lakebed Capsule
**Requested by:** Edgar
**What was done:** Created a new Lakebed capsule folder for the existing GPSA budget-flow HTML using `npx lakebed new`, then adapted the client to host the interactive visualization inside the Lakebed app surface.
**Output:** `gpsa-budget-lakebed/`
**Notes:** Checked Lakebed docs at `lakebed.dev` and `docs.lakebed.dev`. Verified `npx lakebed build . --target anonymous --json` with Node 22, ran Lakebed dev on port 3017, and browser-tested year toggles, line-item mode, and compare animation. Port 3000 was already occupied.

### 2026-05-25 - Claudia delegation reliability audit and doc alignment
**Requested by:** Edgar
**What was done:** Audited Claudia startup, delegation, SOP, manifest, and agent-definition surfaces after delegated audit workers stalled and Edgar explicitly authorized parent-thread completion. Tightened Codex tool-discovery instructions, removed stale manual-fallback language, aligned model metadata to inherited parent execution, clarified portable-output disclosure scope, registered the AI disclosure SOP in the manifest, and cleaned stale Hermes/Eos operational notes.
**Output:** `AGENTS.md`; `_claudia/system/CLAUDIA.md`; `_claudia/system/CODEX_WORKFLOW.md`; `_claudia/system/manifest.json`; `_claudia/sop/delegation.md`; `_claudia/sop/README.md`; `_claudia/sop/output-disclosure.md`; `_claudia/memory/preferences.md`; `_claudia/agent_definitions/*.md`; `_claudia/agents/eos/AGENT_CONTEXT.md`; `_claudia/agents/hermes/AGENT_CONTEXT.md`
**Notes:** Verified manifest JSON parses and all manifest/definition model metadata now uses `inherit_parent`. Remaining fallback references in task logs are historical records, not active routing instructions.

### 2026-05-25 - Repo-wide checkpoint commit and security scan
**Requested by:** Edgar
**What was done:** Prepared a repo-wide checkpoint save, added ignore coverage for raw connector exports and local runtime artifacts, and ran focused pre-commit scans for obvious credential/token leakage before staging.
**Output:** repo commit on `main`
**Notes:** Raw `_claudia/dispatch_inputs/`, Python bytecode, R history, and R workspaces are local-only. High-confidence token/key scans over staged candidate files did not report secrets.

### 2026-05-26 - Minimal Open Brain substrate
**Requested by:** Edgar via Claudia
**What was done:** Added `_claudia/brain.py`, a stdlib SQLite CLI for idempotent Open Brain schema creation, structured event and handoff ingestion, memory and claim rows, concept links, contradictions, basic query, stale and contradiction audit, and Markdown view compilation. Initialized the real `_claudia/claudia.db` with seven empty `brain_*` tables and indexes.
**Output:** `_claudia/brain.py`; `_claudia/system/open-brain.md`; `_claudia/claudia.db`
**Notes:** Production Open Brain tables are present but empty. Smoke tests used a temporary SQLite database for fake rows so the real brain starts clean. Verified syntax, help output, schema creation, DB integrity, event and JSON handoff ingestion, claim audit, query, and Markdown compile.

### 2026-05-27 - Local sqlite-vec Open Brain vector layer
**Requested by:** Edgar via Claudia
**What was done:** Installed local `sqlite-vec` and `pysqlite3`, updated `_claudia/brain.py` to create `brain_vector_items`, `brain_vector_embeddings`, and optional `brain_vec0` vector tables, and added `vector-status`, `vector-index`, and `vector-query` commands. Kept BLOB plus NumPy fallback for runtimes that cannot load SQLite extensions.
**Output:** `_claudia/brain.py`; `_claudia/system/open-brain.md`; `_claudia/claudia.db`
**Notes:** Verified `sqlite-vec` loads through `pysqlite3`, initialized `brain_vec0` in the real Claudia database, and ran an end-to-end temp DB smoke test with Ollama `nomic-embed-text`: claim ingest, sqlite-vec indexing, sqlite-vec query, and BLOB fallback query.

### 2026-05-27 - Automatic Open Brain capture vectorization
**Requested by:** Edgar via Claudia
**What was done:** Changed `_claudia/brain.py` so durable write commands auto-vectorize by default, including events, memories, claims, concept links, contradictions, handoffs, compiled views, and preference capture. Added `capture-preference` so Edgar's durable preferences can be appended to memory, inserted into Open Brain, and embedded in one command.
**Output:** `_claudia/brain.py`; `_claudia/system/open-brain.md`; `_claudia/memory/preferences.md`; `_claudia/claudia.db`
**Notes:** Verified auto-vectorization in a temp SQLite DB for memory ingest, handoff ingest, and preference capture. Captured Edgar's standing preference that Claudia should not require manual `vector-index` after durable Open Brain writes. Use `--no-vectorize` only for offline writes or when Ollama should not be touched.

### 2026-05-27 - Vector dashboard checkpoint
**Requested by:** Edgar via Claudia
**What was done:** Ported the old `embeddings` table into the Open Brain vector layer and scaffolded a local HTTP dashboard server. Added server endpoints for stats, keyword/vector search, migration reruns, health checks, and per-item vector previews.
**Output:** `_claudia/brain.py`; `_claudia/vector_dashboard_server.py`; `_claudia/claudia.db`
**Notes:** Migration completed: 9,130 legacy rows copied into `brain_vector_items`, `brain_vector_embeddings`, and sqlite-vec `brain_vec0`, bringing total vector rows to 9,135. Current pause point: `_claudia/vector_dashboard.html` still needs to be created, then run `python3 _claudia/vector_dashboard_server.py` and open `http://127.0.0.1:8776` in the in-app browser. Latest `vector-status --check-sqlite-vec --json` reported sqlite-vec ready, 9,135 vector items, and source counts of 9,130 legacy embedding rows, 2 handoffs, 2 events, and 1 memory.

### 2026-05-27 — Class Reading Briefs PDF Generation
**Requested by:** Edgar via Claudia
**What was done:** Created a custom Python script `_claudia/scripts/build_one_pagers_pdf.py` using `reportlab.platypus` that parses the Markdown class reading one-pagers in `edgar/2026-05-27_class_reading_one_pagers.md` and generates a beautiful, executive-styled, 7-page vector PDF in `edgar/2026-05-27_class_reading_one_pagers.pdf`.
**Output:** `_claudia/scripts/build_one_pagers_pdf.py`; `edgar/2026-05-27_class_reading_one_pagers.pdf`
**Notes:** The PDF has a professional navy and gold palette, structured course header tables, clean line dividers, a running header and footer with page numbers, and an output disclosure table that adheres strictly to the `output-disclosure` SOP.

### 2026-05-27 — Custom Subagents Configuration for Codex
**Requested by:** Edgar
**What was done:** Created project-scoped custom subagent TOML definitions under the `.codex/agents/` folder for each of the 11 agents defined in the Claudia manifest. Wrote a Python script `_claudia/scripts/generate_codex_agents.py` to programmatically extract and format the configurations from canonical markdown agent definitions, and a validation script `_claudia/scripts/validate_codex_agents.py` to ensure syntactical validity of all generated TOML files.
**Output:** `.codex/agents/*.toml`; `_claudia/scripts/generate_codex_agents.py`; `_claudia/scripts/validate_codex_agents.py`
**Notes:** Verified that all 11 TOML files parsed without a single decode or validation error using Python's standard `tomllib` module. Verified the database connection (`claudia.db`) for Mnemosyne's smoke test and Hephaestus' generation script execution.

### 2026-05-27 - Lean delegated worker startup docs
**Requested by:** Claudia
**What was done:** Updated Claudia Codex delegation docs so parent Claudia still loads the full orchestrator context, while delegated workers load only the lean worker context by default and do not load `_claudia/system/CLAUDIA.md` or `_claudia/system/CLAUDIA_SOUL.md` unless a scoped task requires it. Also documented custom Claudia `spawn_agent` `agent_type` roles versus generic `explorer` and `worker`.
**Output:** `AGENTS.md`; `_claudia/system/CODEX_WORKFLOW.md`; `_claudia/sop/delegation.md`; `_claudia/system/manifest.json`
**Notes:** Verified manifest JSON parses and no repo code references the old generic `startup_required` key.

### 2026-05-27 - Agent label preference update
**Requested by:** Edgar via Claudia
**What was done:** Updated Claudia workflow and preference docs so user-facing agent references use the human/custom agent name only, such as `Athena`, while preserving runtime IDs internally when needed. Removed active instructions to report agents with parenthetical runtime labels.
**Output:** `AGENTS.md`; `_claudia/memory/preferences.md`; `_claudia/system/CODEX_WORKFLOW.md`; `_claudia/sop/delegation.md`; `_claudia/system/manifest.json`
**Notes:** Verified manifest JSON parses and active docs no longer contain the old parenthetical runtime-label dispatch instruction.

### 2026-05-27 - UCSD Gmail CLI account registry
**Requested by:** Edgar
**What was done:** Extended `_claudia/gmail_dispatch_json.py` from a daily-dispatch-only helper into a small CLI for the UCSD Gmail account, with `profile`, `search`, `read`, and `dispatch` commands. Fixed Gmail API query encoding so metadata headers return correctly.
**Output:** `_claudia/gmail_dispatch_json.py`; `_claudia/claudia.db`; `_claudia/agents/mnemosyne/AGENT_CONTEXT.md`
**Notes:** Verified `python3 _claudia/gmail_dispatch_json.py profile` authenticates as `eagunias@ucsd.edu`, `search "emzingo newer_than:180d -in:spam -in:trash" --full` reads the Emzingo interview invitation, and `dispatch --max-results 2 --newer-than 2d` returns real subjects/senders. Added `email_accounts` rows for UCSD Email via local gcloud CLI and Personal Gmail via Codex connector.

### 2026-05-28 - Freeform Sync Automation Refinement and LaunchAgent Setup
**Requested by:** parent
**What was done:** Refined `_claudia/scripts/freeform_sync.py` to support new course mapping shorthands: 'polsea' and 'politics of sea' mapping to 'GPPS 463 - Pol SEA - Ravanilla' (ID: 5), and 'p&s', 'pol/sec', and 'pol:sec' mapping to 'GPCO 410 - Intl Pol:Sec - Praether' (ID: 2). Excluded prior-term class boards 'qm1', 'qm 1', 'qm2', or 'qm 2' from matching 'GPEC 446 - QM3 - Valasquez', routing them to 'Personal Projects' instead. Wrote a macOS LaunchAgent plist at `/Users/edgar/Library/LaunchAgents/com.claudia.freeformsync.plist` to run the sync script every 15 minutes or when the Freeform database (`boards.db` or `Snapshot.plist`) changes, using the explicit `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` interpreter. Loaded, enabled, and kickstarted the background daemon with launchctl, verifying its successful execution in `_claudia/dispatches/freeform_sync.log`.
**Output:** `_claudia/scripts/freeform_sync.py`; `/Users/edgar/Library/LaunchAgents/com.claudia.freeformsync.plist`; `_claudia/dispatches/freeform_sync.log`
**Notes:** Verification logs confirmed that boards containing 'PolSEA' and 'P&S' successfully map to their Spring 2026 classes, while 'QM1' and 'QM2' boards route to Personal Projects.

### 2026-05-29 - 3D Molecular Map view for Open Brain vector dashboard
**Requested by:** Edgar
**What was done:** Added an interactive 3D Molecular Map view to the local Open Brain vector dashboard (`_claudia/vector_dashboard.html`). Created a view toggle in the 3D Map panel, clustered vector items around a large, glowing central "nucleus atom" representing the course, added core atomic structural bonds (lines from satellite nodes to nucleus), and implemented proximity-based semantic cross-links. Fully optimized for high point density (3,000+ nodes) and search result lighting.
**Output:** `_claudia/vector_dashboard.html`; `_claudia/vector_dashboard_server.py`
**Notes:** Changes are active immediately as the local Python server dynamically reads the HTML file on every page request. Verification confirms seamless toggles between Galaxy and Molecular layouts, active hover/click highlights, and search result gravities. Increased the topology nodes database query limit in `_claudia/vector_dashboard_server.py` from 3,000 to 15,000 and restarted the background daemon on port 8776 so that all 9,135+ vector points are rendered in both 3D visualization views.

### 2026-06-01 - Claudia workspace parent folder path audit
**Requested by:** Edgar via Claudia
**What was done:** Updated active hard-coded Claudia workspace paths from `/Users/edgar/Documents/01 Projects/Claudia` to `/Users/edgar/Documents/000 Files` across agent definitions, helper scripts, course utility scripts, skill instructions, and active memory/profile references. Preserved historical old-root paths in prior task logs as provenance.
**Output:** `_claudia/agent_definitions/*.md`; `.codex/agents/*.toml`; `_claudia/scripts/validate_codex_agents.py`; `_claudia/scripts/purge_old_sync.py`; `_claudia/scripts/freeform_ui_sync.py`; `_claudia/scripts/generate_codex_agents.py`; `_claudia/scripts/download_qm3_data_project.py`; `_claudia/skills/mindmapper.md`; `_claudia/agents/hephaestus/AGENT_CONTEXT.md`; `_claudia/memory/edgar-profile.md`; selected course scripts and README files with live absolute paths.
**Notes:** Verified active scripts compile and Codex agent TOML validation passes. Hidden-file scan included `.codex/agents/`. Remaining stale root hits are historical task-log entries only. The external LaunchAgent plist path recorded in memory was not present at `/Users/edgar/Library/LaunchAgents/com.claudia.freeformsync.plist` during this audit.

### 2026-06-01 - PARA workspace reorganization
**Requested by:** Edgar
**What was done:** Reorganized the workspace into PARA: active projects moved under `01 Projects/`, active Spring 2026 course folders moved under `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/`, ongoing admin/personal finance material moved into `02 Areas/`, and reference material moved into `03 Resources/`. Updated Claudia manifest paths, course-agent definitions, generated Codex custom subagent configs, database course/file/reading paths, dashboard output, and Freeform routing for the new layout.
**Output:** `01 Projects/`; `02 Areas/`; `03 Resources/`; `_claudia/system/manifest.json`; `_claudia/system/CLAUDIA.md`; `_claudia/agent_definitions/*.md`; `.codex/agents/*.toml`; `_claudia/claudia.db`; `_claudia/dashboard.html`; `_claudia/scripts/validate_codex_agents.py`; `_claudia/scripts/freeform_ui_sync.py`; `_claudia/scripts/purge_old_sync.py`; `_claudia/agents/hephaestus/AGENT_CONTEXT.md`
**Notes:** Did not spawn subagents per Edgar's instruction. Verified all 11 custom subagent TOML files parse, match manifest agents, and point to existing memory folders with `AGENT_CONTEXT.md`, `FEEDBACK.md`, and `TASK_LOG.md`. Verified manifest and DB course paths resolve, Python scripts compile, root-level course/admin/Personal Projects shells are gone, and active stale path scans are clean. Some historical task-log entries still contain old `/Users/edgar/Documents/01 Projects/Claudia` provenance paths.

### 2026-06-01 - Post-PARA database path validation
**Requested by:** Edgar
**What was done:** Rechecked `_claudia/claudia.db` after Edgar moved additional folders. Updated unambiguous moved paths for the Obsidian knowledge base, GPSA, GPS planning, CalFresh, internship/career files, Breitenfeld assets, course readings, and other uniquely matched indexed files.
**Output:** `_claudia/claudia.db`; regenerated `_claudia/dashboard.html`
**Notes:** SQLite integrity check returned `ok`; foreign key check returned no rows; all course folders resolve; all 11 custom subagent memory paths validate; all `readings.file_path` and `readings.summary_path` rows resolve. Remaining unresolved DB `files.path` rows: 10 stale file-index records for missing generated/legacy artifacts, mostly GPCO 403 Data Brief 1 files, legacy Athena `Claudia/` memory mirror rows, and one old Obsidian generated flashcard note.

### 2026-06-01 - External project archive cleanup
**Requested by:** Edgar
**What was done:** Confirmed completed `01 Projects/` folders were moved outside the workspace, removed the empty local `01 Projects/` shell, marked the remaining project file-index row as `ARCHIVED_OUTSIDE_WORKSPACE/...`, and regenerated the dashboard.
**Output:** `_claudia/claudia.db`; `_claudia/dashboard.html`
**Notes:** No local DB rows still point to `01 Projects/%`. SQLite integrity check returned `ok`. The remaining unresolved local `files.path` rows are the same 10 stale generated/legacy records identified during post-PARA DB validation.
### 2026-06-01 - Mac mini infrastructure scaffold
**Requested by:** Claudia
**What was done:** Added a minimal `_claudia/infra/` scaffold for the Mac mini canonical operations setup, including bootstrap, daily maintenance, Syncthing ignore policy, launchd example, and runbook.
**Output:** `_claudia/infra/README.md`; `_claudia/infra/bootstrap_mac_mini.sh`; `_claudia/infra/daily_maintenance.sh`; `_claudia/infra/syncthing_ignore_template.txt`; `_claudia/infra/launchd/com.claudia.daily-maintenance.plist.example`
**Notes:** Scaffold only. No packages installed, no LaunchAgents loaded, and no destructive file operations performed.

### 2026-06-01 - Mac mini macOS-native infrastructure revision
**Requested by:** Claudia
**What was done:** Revised `_claudia/infra/` so the default Mac mini setup uses macOS-native File Sharing / SMB, SSH, Screen Sharing, Time Machine, launchd, optional Shortcuts, and selected iCloud Drive outputs. Kept Syncthing as an optional later full-mirror path.
**Output:** `_claudia/infra/README.md`; `_claudia/infra/bootstrap_mac_mini.sh`; `_claudia/infra/macos_native_setup_checklist.md`; `_claudia/infra/syncthing_ignore_template.txt`
**Notes:** Documentation and safe script messaging only. No package installs, LaunchAgent loading, file deletion, or system-changing commands performed.
