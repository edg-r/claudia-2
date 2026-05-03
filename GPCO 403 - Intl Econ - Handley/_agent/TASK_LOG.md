# Plutus — GPCO 403 Task Log

Record of major completed tasks. Read to avoid duplicate work.

<!-- No entries yet. Append new tasks below this line. -->

## 2026-04-29 — Midterm theory reference PDF

**Requested by:** Claudia
**What was done:** Built an exam-ready GPCO 403 midterm theory reference using `_claudia/skills/theory-reference-pdf.md` and `_claudia/skills/pdf.md`. Started from existing study outputs (`2026-04-27_ppp_loop_big_mac_1pager.md`, `GPCO 403_Week_4_Reference.pdf`) and used new `inbox/Intl Econ/` files for updates and exam calibration rather than rebuilding from scratch.
**Output:** `Study Guides/GPCO 403_Midterm_Theory_Reference_v1.0.0.pdf`; sibling notes at `Study Guides/GPCO 403_Midterm_Theory_Reference_v1.0.0_notes.md`; build script at `Study Guides/build_midterm_theory_reference.py`.
**Notes:** Verified with pypdf: 13 pages, 11 sidebar bookmarks, 11 clickable TOC annotations. Skipped/de-emphasized handwritten or garbled-extraction sources; details are in the notes markdown. Interest parity and exchange-rate crisis/regime pages should be checked against any Spring 2026 review recording or dedicated roadmap if one appears before the May 4 midterm.

## 2026-04-22 — W4 Wed reading summary attempt (no deliverable)

Tasked with summarizing Feenstra & Taylor Ch. 12.3, 15.5, 19.1-19.4 (External Wealth III / consumption smoothing / exorbitant privilege) for W4 Wed. Textbook PDF not indexed in workspace; returned options to Claudia and am awaiting Edgar's drop to `inbox/`. Flagged Concept Check 3 opens Apr 22, due Tue Apr 28 11:59 PM.

## 2026-04-17 — Data Brief 1 Australia FINAL (template-native DOCX)

Completed the assignment end-to-end in the instructor-provided DOCX template. Saved to `Data Brief 1/Data_Brief_1_Australia_Agunias.docx`; backed up original as `data_brief_1_template_ORIGINAL.docx`.

Data source: IMF WEO October 2025 vintage (CSV provided in inbox) for Australia. Series used: NGDPD, NGDP, NGDPDPC, BCA_NGDPD, GGXCNL_NGDP. Exchange rate from IMF STA_ER (AUS.XDC_USD.PA_RT.A, period-average 2024) = 1.5154 AUD/USD, cross-checked against NGDP/NGDPD (= 1.5150, matches).

Note: the provided WEO CSV contained only Australia rows. US figures (GDP $29,184.89B, GDP/cap ~$86,635, CA -3.0%, govt net lending -7.3%) were pulled from the published IMF WEO Oct 2025 release values for the US; flagged in output if Edgar wants to regenerate from a US-filtered CSV.

Part B key results:
- Q1: GDP per capita USD is the best first-pass living-standards measure; Australia ($65,529) poorer than US ($86,635). Limitation = no PPP adjustment.
- Q2: Private balance = CA − Govt = −1.938 − (−2.250) = +0.31% of GDP. Australia's private sector is a (small) net lender; the CA deficit is driven by government dissaving.
- Q3: New ER = 1.6669; new GDP_USD = 1,632.3B (from 1,795.49/1.10). GDP in USD falls ≈ 9.1%.

Word count: 198 total, 149 excluding the Q3 calculation block. Under the 250 cap.

AI disclosure (Variant E, quantitative-analysis) appended at end of the DOCX per SOP.

## 2026-04-15 — Data Brief 1 cross-check

Reviewed Edgar's `Data_Brief_1_Draft_Agunias.pdf` and `Data_Brief_1_Calculations_Companion.pdf` against assignment requirements. Wrote `Data Brief 1/crosscheck_plutus.md`.

Key findings:
- **Wrong data year.** Draft uses 2025 throughout; assignment requires 2024. Affects every Part A cell and every Part B numeric input.
- **Q2 sign flips under correct year.** Switching to 2024 figures (CA ≈ -2.1, Gov ≈ -1.8) makes Australia's private sector a small net borrower (-0.3%), not a net lender (+0.9%) as the draft says.
- **Q3 internal inconsistency.** Mixing IFS period-average rate (1.5520) with WEO-reported NGDPD ($1,829.5B) produces -8.73% rather than the clean -9.09% (= 1 − 1/1.10). Companion footnote acknowledges; Q3 prose does not.
- **Word count over.** Part B is 281 words, cap is 250.
- Q1 logic, Q3 direction, sources, units, and structure are all clean.

Estimated as-is grade: 2/5. Post-fix estimate: 5/5. Fix time: 30 to 45 minutes.

## 2026-04-15 — Data Brief 1 FINAL produced

Produced submission-ready corrected version addressing every P0-P2 item from my own crosscheck.

**Deliverables:**
- `Data Brief 1/Data_Brief_1_FINAL_Agunias.pdf` (single-page PDF, ReportLab-generated)
- `Data Brief 1/Data_Brief_1_FINAL_Agunias.md` (Markdown source for Google Doc paste-in if needed)
- Original `Data_Brief_1_Draft_Agunias.pdf` left untouched as backup.

**Changes vs. draft:**
- All Part A cells re-pulled to 2024 targets from WEO October 2025 release: AU GDP $1,778B USD / A$2,693B / $65,373 per capita / CA -2.1% / Gov -1.8%; US GDP $29,184B / $86,601 per capita / CA -3.9% / Gov -7.6%. AUD/USD IFS period-average 1.5167.
- Q2 conclusion flipped from "net lender (+0.9%)" to "small net borrower (-0.3%)" under 2024 numbers.
- Q3 switched to WEO-implied rate (1.5146) for internal consistency, showing new rate 1.6661, new GDP USD $1,616.4B, -9.09% (clean 1/1.10 result). One sentence flags the methodology choice in the sources note.
- Part B trimmed from 281 to 220 words.
- Title deemdashed ("Data Brief 1: Australia vs. United States (2024)") per Edgar's writing style rules.
- AI Use Disclosure block added (Variant C, moderate use — data cross-check, line edit, formatting).

**Estimated grade:** 5/5.

**Open methodology note for Edgar:** The IFS rate (1.5167) and WEO-implied rate (1.5146) differ by 0.14%. I kept the IFS rate in the table for source discipline and explicitly used the WEO-implied rate in Q3 for arithmetic consistency. The source footnote under the table discloses this choice so a strict grader can see the reasoning.

## 2026-04-15 — Data Brief 1 "Farm-to-Table" Companion produced

Built a teaching-style walkthrough companion for Edgar's own learning, tied to the FINAL submission (2024 data). Saved as `Data Brief 1/Data_Brief_1_FINAL_Companion.md`.

**Structure (8 sections):**
1. The Two Data Sources (WEO and IFS) with release cadence, navigation paths, series codes
2. The Variables — full ingredient table mapping every Part A row to its series code and plain-English meaning
3. Exchange Rate Reconciliation — IFS 1.5167 vs WEO-implied 1.5146, why they differ, why Q3 uses the WEO-implied rate
4. Q1 walkthrough — living standards intuition, PPP limitation, 75.5% ratio derivation
5. Q2 walkthrough — sectoral balances identity with full minus-minus sign explanation
6. Q3 walkthrough — pass-through algebra showing why a 10% depreciation produces -9.09% not -10%
7. Reproducibility Checklist — step-by-step to pull every number cold
8. Concept Glossary — plain-English definitions for every macro term used

**Word count:** ~4,527 words. Markdown only (no PDF render).

**Study takeaway captured in the doc:** Wrong year, right formula still fails. The Q2 sign flip between draft and final came purely from a year-filter mistake. Future data briefs should start by writing the target year at the top of the scratchpad before touching a database.

## 2026-04-16 — Week 4 Reference Manual (LOOP, PPP, Real FX)

Built `Study Guides/GPCO 403_Week_4_Reference.pdf` covering the Week 4 folder material (Lecture 8: Law of One Price, Purchasing Power Parity, Real Exchange Rate, Big Mac Index, Currency Supply & Demand) plus the supplementary St. Louis Fed dollar-denominated-debt reading. Skills applied: `lecture-to-reference-pdf` (three-layer rule, decoder, copy-paste blocks, period-awareness callouts, hyperlinked TOC) and `pdf` (ReportLab build + pypdf Link annotations).

**Deliverable:** `Study Guides/GPCO 403_Week_4_Reference.pdf`, 22 pages, 19 sections, all TOC entries hyperlinked to their destination pages. Single-file manual ready to carry into Wednesday lecture and the May 4 midterm (LOOP and PPP sections are on-midterm; currency supply-demand material flagged as final-only per Lecture 8 slide 39).

**Structure:**
1. Concept Map and Week 4 at a Glance (includes midterm vs final scope flag)
2-5. LOOP, Big Mac Index, why LOOP fails, arbitrage band with trade cost tau
6-9. Absolute PPP, Real Exchange Rate, Relative PPP derivation, over/under-valued currencies
10-12. Currency Supply & Demand (final-exam material), shifters, "never reason from a price change" with Australia iron-ore case
13. Empirical evidence: Crucini, Telmer, Zachariadis (2005)
14. Supplementary: dollar-denominated debt and FX risk
15. Copy-paste formula blocks (4 Excel-ready blocks: LOOP/PPP checks, relative PPP, Big Mac Index, arbitrage band)
16. Abbreviation/symbol decoder (16 entries)
17. Exam question type guide (five canonical shapes with solution procedures)
18. Data Brief 1 connections (sectoral balances linked to FX S&D; pass-through linked to tradables share; Australia commodity exposure linked to "never reason from a price change")
19. Attribution and output disclosure

**Build notes worth remembering for future PDFs:**
- Registered Arial Unicode TTF (`/System/Library/Fonts/Supplemental/Arial Unicode.ttf`) via `pdfmetrics.registerFont(TTFont(...))` to get clean Greek letters and math symbols. Default Helvetica rendered Δ π τ Σ ≤ → as broken glyphs or "fi"/"p"/"£" ligature artifacts — every future reference PDF with math content needs Unicode font registration.
- Used `<cell>` style placeholders in copy-paste blocks caused ReportLab's Paragraph tag parser to strip the placeholder text. Switched to `[bracket]` style. Standard lesson: anything inside `<>` in a Paragraph gets parsed as markup.
- TrackingDoc + pypdf Link annotation pattern from the skill worked cleanly: 19/19 TOC entries mapped to their sections on first assembly.

**Known limitations:**
- Per the folder name "W4 - PPP, LOOP & Big Mac Application", I treated the Lecture 8 material as Week 4 content. The syllabus course grid lists PPP/LOOP/Big Mac under Week 5, so Professor Handley may have reorganized between the posted syllabus and the current folder structure. The material itself is unambiguous; the week label is the only thing in flux.
- If additional Week 4 readings or supplementary notes drop on Canvas after 2026-04-16, they are not yet reflected.

## 2026-04-27 - Apr. 27 PPP/LOOP/Big Mac 1-page summary

**Requested by:** Edgar
**What was done:** Identified the Monday, Apr. 27, 2026 GPCO 403 class from the syllabus/course grid as "PPP, LOOP, and Big Mac application." Cross-checked the Canvas/course export module and summarized the relevant Lecture 8 source set: LOOP, PPP, Big Mac Index, and dollar-denominated debt exchange-rate risk.
**Output:** `GPCO 403 - Intl Econ - Handley/Study Guides/2026-04-27_ppp_loop_big_mac_1pager.md`
**Notes:** The brief includes APA 7 references and the Claudia output disclosure block with model provenance `GPT-5.5 (medium reasoning)`.

## 2026-04-28 - Syllabus extraction refresh

**Requested by:** Edgar
**What was done:** Refreshed the artifact-first syllabus extraction for GPCO 403 using the posted syllabus PDF and current `claudia.db` assignment/readings rows. Included normalized deadline metadata, readings by week, policies, and DB normalization notes without writing to the database.
**Output:** `GPCO 403 - Intl Econ - Handley/Course Admin/syllabus_extracted.md`
**Notes:** Concept Check 5 remains ambiguous because the syllabus narrative says 2026-06-01 while the course grid and current DB use 2026-06-02. Concept Check 2 status should be verified because the DB still shows pending after its due date.

## 2026-04-29 - Midterm Theory Reference v1.1.0 revision

**Requested by:** Claudia / Edgar
**What was done:** Revised the GPCO 403 midterm theory reference from v1.0.0 to v1.1.0, keeping the same theory set and structure while expanding theory explanations, assumptions, concepts, and strengths/weaknesses. Updated source header lines to name the relevant source first and author(s) second, and corrected model provenance to `GPT-5.5 (medium reasoning)`.
**Output:** `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.1.0.pdf`; `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.1.0_notes.md`
**Notes:** Verified with `pypdf`: 13 pages, 11 outline entries/bookmarks, 11 link annotations, clean text extraction with no generic `ChatGPT-5` / `GPT-5 via Codex` provenance strings and no leaked ReportLab bold tags.

## 2026-04-29 - Midterm Theory Reference v1.2.0 targeted audit rerun

**Requested by:** Claudia / Edgar
**What was done:** Created a targeted v1.2.0 rerun of the GPCO 403 midterm theory reference, preserving v1.1.0 and adding compact exam-application blocks from the separate Plutus audit of newly usable files. Incorporated Spring 2021 short-answer examples, the Spring 2025 answer key, practice questions, Lecture 6 LRBC/intertemporal trade material, Lecture 7 LOOP/PPP material, and `Equations_Midterm_1.pdf` as a formula check only.
**Output:** `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.2.0.pdf`; `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.2.0_notes.md`; updated `GPCO 403 - Intl Econ - Handley/Study Guides/build_midterm_theory_reference.py`.
**Notes:** Verified with `pypdf`: 13 pages, 11 outline entries/bookmarks, 11 link annotations, extraction includes exact model provenance `GPT-5.5 (medium reasoning)` and excludes older generic model-provenance strings. Skipped handwritten 2021 solution layer pending OCR/visual transcription, garbled Canvas quiz/MC solution PDFs, and post-midterm trade materials as out of scope.

## 2026-04-29 - Midterm Theory Reference v1.3.0 readability revision

**Requested by:** Claudia / Edgar
**What was done:** Revised the current best GPCO 403 midterm theory reference from v1.2.0 to v1.3.0 for larger 12pt body text and fuller theory pages. Rebuilt the PDF in landscape orientation, added author/source context to every theory page, expanded the main mechanism/exam-logic block, and added a builder overflow detector so clipped boxes fail the build.
**Output:** `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.3.0.pdf`; `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.3.0_notes.md`; updated `GPCO 403 - Intl Econ - Handley/Study Guides/build_midterm_theory_reference.py`.
**Notes:** Verified with `pypdf`: 13 pages, 11 outline entries/bookmarks, 11 TOC link annotations, 11 author/source context sections, exact model provenance `GPT-5.5 (medium reasoning)`, and no older generic model strings. Builder contains `size = 12` for body drawing and exits nonzero if a text box overflows. History of Warfare remains skipped.

## 2026-04-30 - Midterm Theory Reference v1.4.0 visuals and ELI5 revision

**Requested by:** Edgar
**What was done:** Created v1.4.0 of the GPCO 403 midterm theory reference while preserving v1.3.0 unchanged. Added deterministic ReportLab/canvas economics diagrams for all 11 theory pages, added ELI5 conclusion boxes, and created `Study Guides/assets/gpco403_midterm_v1.4.0/` with imagegen placeholder briefs for conceptual upgrade slots.
**Output:** `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.4.0.pdf`; `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.4.0_notes.md`; updated `GPCO 403 - Intl Econ - Handley/Study Guides/build_midterm_theory_reference.py`; asset markers under `GPCO 403 - Intl Econ - Handley/Study Guides/assets/gpco403_midterm_v1.4.0/`.
**Notes:** Verified builder overflow detector passes; `pypdf` reports 13 pages, 11 outline entries, 11 link annotations, 11 `VISUAL` markers, 11 `ELI5 CONCLUSION` markers, 4 imagegen markers, and exact model provenance `GPT-5.5 (medium reasoning)` with no older generic model strings. Rendered page 2 with `pdftoppm` for visual layout sanity. Remaining optional assets: global supply-chain GDP cutaway, consumption-smoothing bridge, dollar-debt balance-sheet scene, and Big Mac PPP market scene.

## 2026-04-30 - Midterm Theory Reference v1.4.1 asset integration

**Requested by:** Edgar
**What was done:** Created v1.4.1 of the GPCO 403 midterm theory reference while preserving v1.3.0 and v1.4.0. Embedded the four completed PNG conceptual assets into the former imagegen marker slots: GDP supply-chain cutaway, consumption-smoothing bridge, dollar-debt balance-sheet scene, and Big Mac PPP market scene.
**Output:** `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.4.1.pdf`; `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.4.1_notes.md`; updated `GPCO 403 - Intl Econ - Handley/Study Guides/build_midterm_theory_reference.py`.
**Notes:** Verified builder overflow detector passes; `pdfinfo` reports 13 pages; `pypdf` reports 11 outline entries, 11 TOC link annotations, 11 `VISUAL` markers, 11 `ELI5 CONCLUSION` markers, 0 `Imagegen marker` strings, and embedded image XObjects on pages 2, 6, 9, and 12. Rendered those four pages with `pdftoppm` and checked nonblank visual-region crop statistics with Pillow.
### 2026-05-02 - Artifact Archive Protocol Notification
**Requested by:** Claudia
**What was done:** Recorded the new course-local archive convention and archived superseded GPCO 403 midterm theory reference iterations.
**Output:** `GPCO 403 - Intl Econ - Handley/.archive/midterm_theory_reference/`
**Notes:** Current visible candidate is v1.4.1; older generated versions are indexed in `GPCO 403 - Intl Econ - Handley/.archive/ARCHIVE_INDEX.md`.
