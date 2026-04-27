# Athena — GPCO 410 Task Log

Record of major completed tasks. Read to avoid duplicate work.

### 2026-04-27 — Class 9 Walter Ch. 2 one-page summary
**Requested by:** Edgar
**What was done:** Identified Monday Apr 27, 2026 as GPCO 410 Class 9, "Why So Few Negotiated Settlements in Civil Wars," assigned Barbara F. Walter's *Committing to Peace*, Chapter 2, pp. 19-43. Created a concise class-prep summary focused on the credible-commitment logic, demobilization vulnerability, power sharing, and third-party guarantees.
**Output:** `GPCO 410 - Intl Pol:Sec - Praether/Study Guides/class9_walter_committing_to_peace_ch2_1page_summary.md`
**Notes:** Used the syllabus, local Walter PDF/OCR artifact, and existing Athena theory-reference notes. The OCR text for the local PDF is visually recoverable but text extraction remains garbled; existing theory-reference notes remain the cleanest local extraction layer.

## 2026-04-24 — ORANGE Memo (Myanmar) full draft
- Produced full-length first draft at `Assignments/Orange Memo - Myanmar/Orange_Memo_Myanmar_DRAFT.docx` via `build_memo.py` (python-docx; Times New Roman 12pt, double-spaced, 1-inch margins per syllabus).
- Six body paragraphs + closing sentence; 947 body words (under 950 graded ceiling). Per-paragraph: 88 / 145 / 207 / 77 / 218 / 183 / 29 — matches the kickoff `orange_memo_kickoff.md` 950-word budget within ~5-word tolerance.
- Thesis locked per kickoff: 2010 opening raised risk, 2021 coup realized it. Cederman + Walter as the theory pair; Powell as unifying-mechanism vocabulary (not three-type taxonomy per FEEDBACK 2026-04-14).
- Ali 90/100 feedback applied structurally: P3 names full Tatmadaw strategy set (continued junta rule / genuine transfer / disciplined-democracy veto) with rejection reasons; P5 walks actors-preferences-strategies-beliefs-payoffs visibly and carries the dedicated why-no-settlement beat with concrete bargaining terms (Art. 436 amendment for military carve-outs + immunity).
- Praether screens passed: no "miscalculation in game theory", no misuse of "two-level game", 2010 vs 2021 dates stamped separately, Cederman's democratization vs governmental-conflict findings kept distinct.
- Footnotes drafted as a numbered list at the tail of the document with the superscript markers 1–11 embedded inline in the body. **python-docx limitation: these are not live Word footnotes yet.** Edgar needs to either (a) convert manually in Word (Insert → Footnote on each superscript marker) or (b) ask Hephaestus for an OOXML pass that rewrites the superscripts into live footnote references against the document's footnotes part.
- Open items flagged for Edgar voice pass: (1) full AI-assisted text must be rewritten in Edgar's voice per syllabus AI policy (no AI-generated prose may be submitted verbatim); (2) ai-disclosure block per `_claudia/sop/ai-disclosure.md` appended before Canvas upload; (3) footnote conversion; (4) optional title tweak; (5) verify Constitution article numbers and NLD 2020 seat counts against a primary source before footnote freeze.

## 2026-04-24 — Polity IV / Regime Type data memo outline (Myanmar 2000–2018)
- Built outline-only deliverable at `Assignments/Data Memo - Regime Type/Data_Memo_RegimeType_Myanmar_OUTLINE.md`.
- Anchored to Polity5 v2018 extract already pulled 2026-04-20 (see `data_pull_status.md`): trajectory -6 (2000–2010) → -3 (2011–2014) → -88/interp. 2 (2015) → +8 (2016–2018); driven by `xconst` 1–2 → 3 → 7 and `parcomp` 1–2 → 4.
- Structure: BLUF + 6 sections (Framing, Data/Measurement, Trajectory 3.1–3.4, What Polity Captures/Misses, Implications, Open Questions) + Figures 1–2 + Table 1 + draft-stage checklist.
- Analytical payoff preloaded: component-level reading shows Polity is capturing constitutional form, not the Tatmadaw veto that later realizes in the 2021 coup (out of sample) — bridges cleanly back to the ORANGE memo commitment-problem thesis if Edgar wants that link.
- Open blockers for Edgar: (1) thesis-direction choice a/b/c; (2) codebook page cites for xconst=7 / parcomp=4; (3) V-Dem or FH second-dataset decision; (4) post-2018 framing scope; (5) word/page cap confirm.


## 2026-04-23 — Class 8 theory-reference PDFs (new default format)
- Produced theory-reference PDFs (supersedes BLUF for reading prep per `feedback_reading_summary_format.md`):
  - `Study Guides/walter_ch2_theory_reference.pdf` — ANCHOR (7 pp)
  - `Study Guides/bueno_de_mesquita_et_al_institutional_dp_theory_reference.pdf` — ANCHOR
  - `Study Guides/fearon_audience_costs_theory_reference.pdf` — ANCHOR
  - `Study Guides/herrmann_tetlock_visser_mass_public_theory_reference.pdf` — standard
- Blocker: Cederman/Hug/Krebs PDF not in workspace; awaiting Edgar's Canvas drop to `inbox/`.
- Cross-ref: Memo 2 Ali feedback (90/100) logged 2026-04-23 entry below; Orange kickoff already augmented with framework-to-paragraph mapping.

## 2026-04-23 — Memo 2 grade ingest (Ali, 90/100) + Orange kickoff augmentation
- Captured Ali's strategic-choice-framework feedback as durable rule in FEEDBACK.md and pointer in COURSE_MEMORY.md.
- Augmented `Assignments/Orange Memo - Myanmar/orange_memo_kickoff.md` with an "Ali feedback integration" section mapping the 5 framework elements to the 6 planned paragraphs, flagging where strategy alternatives + beliefs + expected payoffs must appear, and carving dedicated "why no settlement" depth.

## 2026-04-22 — Class 8 reading summaries (Walter + Blattman-Miguel) + W4/W5 misfile flag
- Flagged both PDFs as misfiled under `W5 - Negotiated Settlements & Democratization/` despite being W4 Class 8 readings per syllabus. File-naming drift from Canvas; do not move without Edgar's sign-off.

## 2026-04-22 — Class 8 reading summaries (Walter + Blattman-Miguel) [original]
- Task: BLUF memo summaries for both required readings for Class 8 (Apr 22): Explaining Civil Wars.
- Output:
  - `Study Guides/walter_2009_bargaining_failures_civil_war_summary.md`
  - `Study Guides/blattman_miguel_2010_civil_war_summary.md`
- DB: `readings` rows for Walter "Bargaining Failures and Civil War" and Blattman-Miguel "Civil War" marked summary_status=completed with paths.
- Note: Both PDFs live in `W5 - Negotiated Settlements & Democratization/` despite being W4 Class 8 readings per syllabus (file-naming drift from Canvas).

## 2026-04-20 — Polity data pull for Regime Type memo
- Task: Complete the mechanical setup for `Assignments/Data Memo - Regime Type/` by acquiring the live CSP Polity materials, extracting Myanmar country-year data, and documenting the pull.
- Output:
  - `Assignments/Data Memo - Regime Type/polity5_v2018_timeseries.xls`
  - `Assignments/Data Memo - Regime Type/polity5_v2018_codebook.pdf`
  - `Assignments/Data Memo - Regime Type/systemicpeace_inscrdata_access_page.html`
  - `Assignments/Data Memo - Regime Type/myanmar_polity5_2000_2018.csv`
  - `Assignments/Data Memo - Regime Type/data_pull_status.md`
- Key result: live CSP links still resolve to `p5v2018`; Myanmar (`ccode 775`) runs `-6` through 2010, `-3` in 2011-2014, `-88 / polity2=2` in 2015, and `+8` in 2016-2018.
- Constraint carried forward: the public Polity file still ends at 2018, so the 2021 coup remains out of sample for this memo unless another dataset is introduced.

## 2026-04-16 10:55 PT — Week 4 Reference PDF (Democratic Peace & Civil War)
- Task: Build a theory-reference PDF for Week 4 before next week's class (Class 7 Apr 20, Class 8 Apr 22). Three-layer claim/mechanism/anchor structure per `_claudia/skills/lecture-to-reference-pdf.md`.
- Output: `GPCO 410 - Intl Pol:Sec - Praether/Study Guides/GPCO_410_Week_4_Reference.pdf` — 14 pages, hyperlinked TOC, ReportLab + pypdf build per skill mechanics.
- Coverage: (1) Bueno de Mesquita et al. 1999 (core, Class 7 DPT); (2) Walter 2009 (core, Class 8 civil war); (3) Blattman & Miguel 2010 (core, Class 8 civil war survey); (4) Fearon 1994 Audience Costs (supplementary, in W4 folder but not syllabus-assigned); (5) Herrmann/Tetlock/Visser 1999 (supplementary, in W4 folder but belongs to W10 Public Opinion module).
- File-misfile note carried over from morning audit: Walter 2009 and Blattman & Miguel 2010 are physically in `W5 - Negotiated Settlements & Democratization/` but the syllabus assigns them as Week 4 Class 8 readings. Flagged in the PDF's File & OCR Notes section.
- OCR status: all 5 W4 readings extract cleanly via `pdftotext` (BdM 109k chars / 18pp; Walter 85k / 21pp; Blattman & Miguel 229k / 55pp; Fearon 97k / 17pp; Herrmann et al. 111k / 21pp). No OCR work required.
- Structure: Cover + TOC, W4 at a Glance, syllabus prompts, theory-tracking callouts (Fearon 1995, Powell 2006, Fearon 1994 — all carryover from W1–W3), per-reading BLUF + claim/mechanism/anchor tables, author-argument decoder (8 authors), 14-term key-concepts table, concept map linking W4 to W1–W3 and W5, ORANGE memo deployment guide for Options A (South America) and B (Muslim civil wars) since syllabus-listed W4 memo prompts are live even though Edgar is skipping per strategy brief, disclosure.
- Consistency with morning strategy brief: PDF explicitly flags that Edgar is skipping both W4 ORANGE options for Myanmar (W5); Week 4 material is treated as midterm fuel + background for Myanmar memo, not a writing target. Memo traps section pulls from FEEDBACK.md.
- Concurrency: wrote only to `Study Guides/`. Did not touch `Memo 2 - Myanmar/` or `Data Memo - Regime Type/` folders being worked by the parallel Athena instance. Build script at `/tmp/build_w4_reference.py`.
- Compliance: output-disclosure SOP block in the PDF (section 14); both lecture-to-reference-pdf and pdf skills invoked and cited in the method line.

## 2026-04-16 — ORANGE Memo (Myanmar) + Data Memo (Regime Type) groundwork scaffolded
- Task: Edgar greenlit the pre-midterm picks. Spin up both project folders with prompt, reading notes, context/data plan, and outline files. Keep the two projects strictly separated.
- Folders created (under `Assignments/` to match Blue Memo convention):
  - `Assignments/Orange Memo - Myanmar/` — 4 files: `prompt.md`, `reading_notes.md`, `myanmar_context.md`, `outline.md`
  - `Assignments/Data Memo - Regime Type/` — 4 files: `prompt.md`, `data_plan.md`, `reading_notes.md`, `outline.md`
- Verbatim prompts pulled from the full syllabus PDF (`Course Admin/International_Politics_and_Security_Syllabus.pdf`), NOT from the smaller Canvas TOC PDF. Source paths cited in each `prompt.md`.
- Reading notes follow `_claudia/skills/memo-summarizer.md` — BLUF, Context & Scope, Key Evidence, Implications, Limits. Summaries built from direct `pdftotext` extraction of Cederman, Walter "Bargaining Failures", and Meng & Little — not from recall.
- Shared-reading separation: Cederman Hug & Krebs has full notes in the Orange memo file (primary role: theoretical anchor). Data memo reading_notes.md cross-references that file and describes Cederman's separate role in the data memo (exemplar Polity user whose findings depend on Polity coding). Meng & Little lives only in the data memo folder. Walter and Powell live only in the Orange memo folder. No duplication.
- Myanmar context brief (`myanmar_context.md`) covers actors (Tatmadaw, NLD, NUG, PDF, EAOs, China, ASEAN), 1962–2025 timeline (compressed), Polity IV coding history, mechanisms the memo must address (Cederman/Walter/Powell), evidence pegs with constitutional article numbers, and sources.
- Data plan (`data_plan.md`) locates Polity5 at Center for Systemic Peace, provides direct download URLs (`https://www.systemicpeace.org/inscr/p5v2018.xls` and `p5manualv2018.pdf`), names variables (`polity`, `polity2`, `democ`, `autoc`, `xconst`, `parcomp`, `durable`), explains special codes (−66/−77/−88), flags the Polity5 v2018 coverage gap at 2018 (post-coup years out of sample), and recommends pivoting the memo to the 2010–2015 partial-democratization coding rather than the 2021 coup to stay in-sample.
- Outlines: both first-draft, thesis placeholder, 5–7 body beats each, word budgets sized against the 950-word grading ceiling, evidence/footnote plan, pre-flight screens built on Athena FEEDBACK.md (Praether writing traps). Edgar to sign off on thesis direction before prose drafting.
- Deadline discrepancy flagged in both prompts: syllabus pp. 2, 10 suggest Apr 29 / 11:00am; Canvas TOC and `claudia.db` id 31 show May 15 / 5:00pm for Data Memo Regime Type (Prather moved the date). TODO for Edgar to confirm with Prather or TA.
- Orange-count discrepancy flagged in both prompts: syllabus lists 4 ORANGE options (South America DPT, Muslim civil wars, FARC, Myanmar), not 3. TODO for Edgar.
- Compliance: every deliverable file closes with the disclosure block per `_claudia/sop/output-disclosure.md`. Memo-summarizer skill explicitly invoked on both reading_notes files.

## 2026-04-16 — Pre-midterm strategy brief (ORANGE memo + Data memo)
- Task: Build a strategy recommendation covering (a) which ORANGE analytic memo topic to pick from the four syllabus options, (b) which data memo topic to pair with it, (c) timeline through midterm (4 May).
- Output: `GPCO 410 - Intl Pol:Sec - Praether/Study Guides/pre_midterm_strategy.md`
- Recommendation: **Myanmar ORANGE memo (Week 5, Class 10, due 29 Apr)** + **Regime Type (Polity IV) data memo (due 15 May)**. Rationale: SEA regional fit (Edgar's FSO track + GPPS 463 knowledge), reading tractability (Cederman et al. OCR-clean), and direct synergy between the two deliverables (Myanmar's Polity IV coding history is the data memo's case).
- Reading tractability audit (via `pdftotext`): FARC Walter Ch. 2 PDF is image-only (15 chars over 15 pages) — OCR required before usable. This downgrades Option C (FARC). Cederman (W6 folder), Walter "Bargaining Failures" (misfiled in W5, actually Week 4 Class 8 reading), Bueno de Mesquita, Blattman/Miguel, and Meng/Little are all OCR-clean.
- File misfilings flagged: "Week 5-Walter.pdf" is actually the Week 4 Class 8 Walter paper; "Week 4-Fearon.pdf" is actually the Week 10 Fearon "Domestic Political Audiences" paper; Cederman sits in the W6 folder rather than W5. Not blocking the recommendation but worth a sweep later.
- Syllabus vs. Edgar's "three options" framing: syllabus lists FOUR ORANGE options (South America DPT, Muslim civil war, FARC, Myanmar). Brief covers all four and recommends Myanmar. Flagged the count discrepancy for Edgar to confirm with Praether or TA.
- Timeline: ORANGE draft locked Sat 25 Apr, submit Wed 29 Apr; data memo framing starts Thu 30 Apr; midterm prep weekend 3 May; midterm 4 May; data memo polish through 15 May.

## 2026-04-15 — Memo 1 FINAL integration (Edgar's accept/reject decisions applied)
- Task: Build `Memo 1 - Oil and Water_FINAL.docx` from FOOTNOTES base, applying Edgar's decisions from his annotated `Memo 1 - Athena Proofread.md`. Clean copy, no tracked changes, footnotes intact.
- Accepted line edits: 1.1 (thesis — only "miscalculation in game theory" swapped to "a misread of capabilities"), 1.2 (Bush/they antecedent), 1.4 (Hussein's WMD capability), 1.9 (apostrophe + "two-level game" → "dual-audience signaling"), 1.10 (decade of noncompliance), 1.12 (all mechanics fixes). Kept originals on 1.3, 1.5, 1.6, 1.7, 1.8, 1.11.
- Accepted developments: A (Iran deterrence lock-in, Hussein paragraph), B (operationalized inefficiency condition, synthesis paragraph), C (rejecting information alternative, end of framework paragraph), D (Woods et al. internal regime finding, Hussein paragraph, attached to new shortened footnote 3).
- Accepted Q3 short variant (~80 words) inserted as new paragraph between synthesis and conclusion.
- Final body word count: 972 (up from 829). At standard ~250 words/double-spaced page: ~3.9 pages body, plus cover and references = ~5.5 pages total. OVERFLOWS 3-page ceiling materially. Flagged to Edgar with triage options.
- Method: Direct XML manipulation of `word/document.xml` and `word/footnotes.xml` inside the docx zip, preserving all existing footnote references and run structure for voice-preserved paragraphs.

## 2026-04-15 — Memo 1 substance audit: sub-question 3 gap
- Task: Audit Edgar's Memo 1 "Oil and Water" (FOOTNOTES.docx) for coverage of prompt sub-question 3 (counterfactual settlement terms + mechanism for non-signability)
- Finding: Memo answers (1) "no, settlement not possible" and (2) "why: Powell commitment problem." Sub-question 3 underdeveloped — the "cost of credible commitment was simply too high" paragraph gestures toward the counterfactual but does not specify deal terms or the non-fungibility mechanism.
- Output: `Assignments/Blue Memo/Memo 1 - Oil and Water_ATHENA_ADDITION.docx` — preferred ~150-word insertion (four-term settlement bundle + Powell Type-2 mechanism), ~80-word short variant for 3-page ceiling, and optional one-line thesis patch
- Mechanism invoked: Powell Type 2 (bargaining over the distribution of power itself). Verifiable disarmament was itself the power-shifting concession — compliance strips Saddam of Iranian deterrent ambiguity, coup-proofing premium, and residual leverage, leaving a preventive-doctrine Bush administration free to press on to regime change. No side-payment restores that position; no Bush pledge binds the next decision cycle. Closes Fearon loop: even under full information the deal fails because the problem was never information — it was the non-fungibility of the concession demanded.
- Parallel work: Calliope running line-edit pass on FOOTNOTES.docx concurrently; addition kept as separate companion doc for later splice.

## 2026-04-14 — Memo 1 proofread applied as Word tracked changes
- Task: Build `Memo 1 - Oil and Water_TRACKED.docx` with all Top 3 priority edits + line edits 1.2, 1.4-1.11, 1.12 as `w:ins`/`w:del` revisions (author="Athena", date=2026-04-14), and Word comments at Development B/C/D insertion points
- Files:
  - Original (untouched): `Assignments/Blue Memo/Memo 1 - Oil and Water.docx`
  - Tracked-changes output: `Assignments/Blue Memo/Memo 1 - Oil and Water_TRACKED.docx` (18,830 bytes)
  - Build script: `/tmp/build_tracked.py`
- Method: Unzipped docx, manipulated `word/document.xml` by replacing exact run-sequence needles with paired `w:del`/`w:ins` blocks. Added `word/comments.xml` with three comments (IDs 2001, 2002, 2003) and wired `commentRangeStart`/`commentRangeEnd`/`commentReference` into document.xml. Registered the new part in `[Content_Types].xml` and `word/_rels/document.xml.rels`. Rezipped with `[Content_Types].xml` first per OPC.
- Verification: 11 `w:ins` and 11 `w:del` pairs (all Athena), 3 matched comment triples, all original problematic phrases preserved in `w:delText` so rejecting a revision restores the original. XML well-formed across document.xml, comments.xml, Content_Types, and rels. `textutil` renders the accepted-all-revisions view correctly.
- Skipped intentionally: Developments B, C, D prose additions (per instructions — only the Iran-deterrence Development A was applied, combined with Edit 1.5 cut). Those three appear as margin comments for Edgar to decide on.

## 2026-04-14 — Powell (2006) commitment problems study guide
- Task: Produced study guide on Powell's three types of commitment problems for exam prep
- Output: Inline response — named types, scope conditions, canonical examples, comparison table, unifying insight
- Sources: Atlas theory reference PDF (W3 folder), Powell 2006 IO 60(1)
- THEORIES.md updated with full Powell entry (Type 1, 2, 3 + key terms + cross-references)

## 2026-04-14 — Memo 1 APA-to-footnotes conversion
- Task: Convert Memo 1 "Oil and Water" from APA in-text citations to Chicago/Turabian footnotes; add APA 7 References page
- Files:
  - Original (untouched): `Assignments/Memo 1 - Oil and Water.docx`
  - APA backup: `Assignments/Memo 1 - Oil and Water_APA-backup.docx`
  - Working copy (footnotes): `Assignments/Memo 1 - Oil and Water_FOOTNOTES.docx`
- Method: Direct OOXML edit (python-docx lacks first-class footnote support). Unzipped docx, surgically replaced two citation runs in `word/document.xml` with `<w:footnoteReference>` markers, appended two full-note Chicago entries to `word/footnotes.xml`, inserted two APA 7 reference paragraphs before the `<w:sectPr>` block. Repacked with zipfile.ZIP_DEFLATED.
- Citations converted: 2 (both first-mention, both full Chicago notes)
  1. (Powell, 2006) → note 1: Robert Powell, "War as a Commitment Problem," International Organization 60, no. 1 (2006): 169–203.
  2. (Woods, Lacey & Murray, 2006) → note 2: Kevin M. Woods, James Lacey, and Williamson Murray, "Saddam's Delusions: The View from the Inside," Foreign Affairs 85, no. 3 (2006): 2–26.
- Unique sources in References: 2 (Powell; Woods, Lacey & Murray), alphabetical
- Prose preserved verbatim (verified paragraph-by-paragraph against original extraction). Only change inside prose: periods now sit before the footnote marker per Chicago convention — the period characters themselves were already in Edgar's text.
- XML validation: all three modified parts (document.xml, footnotes.xml, [Content_Types].xml) parsed cleanly post-edit.

## 2026-04-16 — Pre-midterm strategy brief (memo + data memo recommendations)
- Task: Produce a GPCO 410 pre-midterm strategy. Evaluate all ORANGE memo options and analytical essay options. Rank by reading tractability (which PDFs are OCR-extractable vs scan-only) and fit-to-Edgar (SEA/FSO wheelhouse, existing GPPS 463 context).
- Output: `Study Guides/pre_midterm_strategy.md`
- Picks:
  - **ORANGE memo: Myanmar (Week 5, Class 10, due Apr 29)** — only SEA-track option, readings clean (Cederman extracts fine), FARC option blocked by scan-only Walter Ch. 2 PDF (15 extractable chars across 15 pages, needs OCR).
  - **Data memo: Regime Type / Polity IV (due May 15)** — pairs directly with Myanmar's 2010-2021 coding whipsaw, and Cederman + Meng/Little do double duty across both deliverables.
- Flag: syllabus lists four ORANGE options not three. TODO for Edgar to verify with Praether/TA at next class.

## 2026-04-16 — Myanmar memo + Polity IV data memo groundwork
- Task: Build project folders with prompts, reading notes, context briefs, and outlines for both deliverables. Keep strictly separated — Edgar flagged that explicitly.
- Output (Myanmar):
  - `Assignments/Orange Memo - Myanmar/prompt.md` (verbatim Week 5 Class 10 prompt from syllabus PDF)
  - `Assignments/Orange Memo - Myanmar/reading_notes.md` (Cederman/Hug/Krebs primary anchor, Walter 2009 commitment-problem complement, Powell 2006 background)
  - `Assignments/Orange Memo - Myanmar/myanmar_context.md` (actors, 1962-2025 timeline, Polity coding history, four mechanisms, evidence pegs)
  - `Assignments/Orange Memo - Myanmar/outline.md` (thesis placeholder, 7 beats, 1,300-word draft budget with 950-word ceiling, Praether-trap pre-flight screens)
- Output (Data memo):
  - `Assignments/Data Memo - Regime Type/prompt.md` (verbatim rubric + Week 5 regime-type listing)
  - `Assignments/Data Memo - Regime Type/data_plan.md` (CSP Polity5 URLs, variables, special codes)
  - `Assignments/Data Memo - Regime Type/reading_notes.md` (Meng/Little as primary measurement critique)
  - `Assignments/Data Memo - Regime Type/outline.md` (three central-question options A/B/C, 6 beats mapped to rubric's 9 questions)
- **Structural blockers flagged in both prompt.md files:**
  1. Polity5 v2018 stops at 2018 — Myanmar's 2021 coup out-of-sample. Recommend pivoting data memo to the 2010-2015 partial-democratization coding instead.
  2. Data memo deadline conflict: syllabus says Apr 29 11am, Canvas + `_claudia/claudia.db` say May 15 5pm.
  3. ORANGE options count: 3 vs 4 discrepancy carried forward from strategy brief.

## 2026-04-16 — Week 4 theory-reference PDF
- Task: Build `GPCO_410_Week_4_Reference.pdf` covering Class 7 (Mon Apr 20 Democratic Peace) + Class 8 (Wed Apr 22 Civil War).
- Output: `Study Guides/GPCO_410_Week_4_Reference.pdf` (14 pages, hyperlinked TOC)
- Readings found: Bueno de Mesquita et al. 1999, Walter 2009, Blattman & Miguel 2010, plus local extras (Fearon 1994, Herrmann/Tetlock/Visser 1999). All 5 OCR-clean via pdftotext — no OCR work required.
- File misfile note: Walter and Blattman/Miguel are physically in the W5 folder, not W4. Flagged inside the PDF itself.
- Structure: cover + BLUF card, W4 at a Glance, theory-tracking callouts carrying Fearon 1995 / Powell 2006 / Fearon 1994 forward from W1-W3, per-reading BLUF + claim/mechanism/anchor tables, 8-author decoder, 14-term concepts table, concept map to W1-W3 and W5, ORANGE memo deployment guide for Options A (South America) and B (Muslim civil wars), file/OCR notes.
- Memory-folder convention note: this course uses `Claudia/` as Athena's memory subfolder, not `_agent/` like the other four courses. Per-course variation, not a bug. Both conventions are legitimate.

## 2026-04-20 — Orange Myanmar memo kickoff scaffold
- Task: Convert the Myanmar ORANGE memo outline into a drafting-ready kickoff file without drafting the memo itself.
- Output: `Assignments/Orange Memo - Myanmar/orange_memo_kickoff.md`
- What was locked: final thesis choice, all four open outline decisions, a tighter 6-paragraph macro structure with paragraph purposes/evidence pegs/likely footnote anchors, and a trimmed 950-word target budget.
- Key carry-forward choice: use the thesis that the 2010 opening raised civil war risk and the 2021 coup realized that risk; keep Rohingya as a short standalone proof paragraph rather than a full heavy beat.

### 2026-04-20 — Orange Memo TA-Email Draft
**Requested by:** Claudia (on Edgar's instruction)
**What was done:** Drafted a three-sentence clarification email asking the GPCO 410 TA whether the Cederman/Hug/Krebs "Democratization and Civil War" piece (filed in Canvas under `Week 6-Democratization and Civil War.pdf`) is the intended Class 10 Myanmar reading for the Orange memo, and whether additional Class 10 readings should be incorporated. Addressed with last-name-plus-title placeholder per correspondence-formality rule. No emdashes. Short (3-4 sentences).
**Output:** `GPCO 410 - Intl Pol:Sec - Praether/Assignments/Orange Memo - Myanmar/ta_email_draft.md`
**Notes:** Important catch — no TA is named in the syllabus, COURSE_MEMORY.md, or SYLLABUS_NOTES.md. Prather is listed as sole instructor. Flagged to Edgar that he needs to fill in the TA name from Canvas before sending, or redirect the message to Prather directly. Update COURSE_MEMORY.md with TA info when Edgar confirms.

## 2026-04-24 — Orange Memo Myanmar full draft

**Requested by:** Claudia (on Edgar's instruction)

**What was done:** Drafted the full Orange Memo from the kickoff scaffold. 947 body words against the 950 ceiling, Times New Roman 12pt double-spaced 1" margins. Six paragraphs plus closing, Ali-feedback beats loaded visibly: P1 answer + Cederman/Walter frame, P2 theory spine (Cederman democratization-risk + governmental-conflict distinction, Walter commitment problem, Powell as unifying mechanism), P3 2008 constitution as incomplete democratization with Tatmadaw's full strategy set (junta rule / transfer / disciplined-democracy veto) and dominance reasoning, P4 Rohingya as proof reforms never bound Tatmadaw, P5 2020 trigger with full actors-preferences-strategies-beliefs-payoffs walk plus dedicated why-no-settlement beat, P6 post-coup war + stability-narrative rebuttal + generalizable policy implication, closing lands the causal inversion. Footnote markers 1-11 embedded as superscript numerals in body, full footnote text listed at tail (python-docx cannot create live Word footnote fields).

**Output:** `/Users/edgar/Documents/01 Projects/Claudia/GPCO 410 - Intl Pol:Sec - Praether/Assignments/Orange Memo - Myanmar/Orange_Memo_Myanmar_DRAFT.docx` plus `build_memo.py` rebuild script.

**Notes:** Handed cleanly to Calliope for aggressive voice pass (AI-source, not Edgar-written). Remaining manual items for Edgar before Canvas: convert footnote markers to live Word footnote fields (manual Insert→Footnote or Hephaestus OOXML), paste AI-disclosure block per `_claudia/sop/ai-disclosure.md`, verify 2008 Constitution article numbers (109(b)/141(b)/417/436) and NLD 2020 seat counts (258/315, 82%), replace placeholder title. Syllabus forbids AI prose verbatim so every paragraph needed Edgar's voice pass per `feedback_voice_pass_ai_source.md` — Calliope handled it same session.

## 2026-04-24 — Polity IV Data Memo outline

**Requested by:** Claudia (on Edgar's instruction)

**What was done:** Outline-only deliverable for the Polity IV / Regime Type Data Memo on Myanmar 2000-2018. Skeleton: BLUF placeholder (three thesis options pending Edgar's pick), §1 Framing (why Myanmar 2000-2018, flag 2018 cutoff up front), §2 Data and Measurement (Polity5 v2018, ccode 775, 19 obs, key variables, polity2 interpolation note), §3 Myanmar Trajectory four-phase core empirical (entrenched autocracy 2000-2010, anocratic opening 2011-2014, transition 2015, codified democracy 2016-2018), §4 What Polity Captures/Misses (component decomposition: xconst + parcomp carry the move, recruitment side flat), §5 Implications for Measuring Regime Type, §6 Open Data Questions. Plus Figures 1-2, Table 1, optional Table 2, draft-stage checklist, disclosure block.

**Output:** `/Users/edgar/Documents/01 Projects/Claudia/GPCO 410 - Intl Pol:Sec - Praether/Assignments/Data Memo - Regime Type/Data_Memo_RegimeType_Myanmar_OUTLINE.md`

**Notes:** Six decisions returned to Edgar before drafting can start: (1) thesis direction — component-level diagnosis of what Polity measures [default lean], cross-dataset triangulation with V-Dem/Freedom House, or bridge back to Orange's commitment-problem thesis with one-sentence (c) bridge; (2) codebook page cites for `xconst=7` and `parcomp=4` from `p5manualv2018.pdf`; (3) V-Dem or Freedom House triangulation only if §4 needs it; (4) `change`/`d5`/`sf` flag audit; (5) post-2018 framing of 2021 coup as measurement stress test, or stay strictly in window; (6) confirm 3-page cap per Praether convention from FEEDBACK.md 2026-04-14. Drafting scheduled for Sun Apr 26 11:00-13:00 on Learning calendar.
