# Tyche — GPEC 446 Task Log

Record of major completed tasks. Read to avoid duplicate work.

<!-- No entries yet. Append new tasks below this line. -->

### 2026-04-30 — QM3 midterm lecture reference sheet v1.2.1 patch
**Requested by:** Edgar
**What was done:** Created the v1.2.1 patch while preserving v1.2.0 unchanged. Updated the builder to target v1.2.1 outputs and wrap long formula/code lines inside the page margins using 10.5pt Courier for formula blocks only; expanded Conditional Independence Assumption (CIA) on first use; added one short "Explain Like I'm 5" conclusion for each of the 12 numbered topics.
**Output:** `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Lecture_Reference_v1.2.1_notes.md`; `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Lecture_Reference_v1.2.1.pdf`; updated `GPEC 446 - QM3 - Valasquez/Study Guides/build_qm3_midterm_lecture_reference.py`
**Notes:** Verification used `pdftotext`, `pdfinfo`, PyMuPDF span bounds, and rendered page images for the widest formula pages. The widest Courier/formula span ended at x=536.1 pts on a 612-pt letter page, with no non-footer text beyond the right content threshold; the PDF has 26 pages, extractable CIA expansion, 12 ELI5 conclusions, and the output disclosure at the end.

### 2026-04-30 — QM3 midterm lecture reference sheet v1.2.0 readability and visuals
**Requested by:** Edgar
**What was done:** Created the next iteration of the lecture-based midterm reference sheet while preserving v1.1.0 outputs. Copied the v1.1.0 notes into v1.2.0, kept the narrative/exam-facing structure and first-use acronym pattern, retargeted the builder to generate v1.2.0 with 12pt body/table/code text and 1-inch margins, and added original ReportLab-generated visual aids for potential outcomes, OLS, OVB, bad controls, IV/Wald/LATE, compliance types, and assumptions.
**Output:** `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Lecture_Reference_v1.2.0_notes.md`; `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Lecture_Reference_v1.2.0.pdf`; updated `GPEC 446 - QM3 - Valasquez/Study Guides/build_qm3_midterm_lecture_reference.py`
**Notes:** Verification confirmed the v1.2.0 PDF has 24 pages, extractable text, disclosure at the end, all seven visual-aid captions present, and builder settings for 12pt content plus 1-inch margins. Rendered spot checks of pages 4, 19, 21, and 23 caught and fixed two diagram title overlaps before the final PDF was regenerated.

### 2026-04-30 — QM3 midterm lecture reference sheet v1.0.0
**Requested by:** Edgar
**What was done:** Built a new lecture-slide-based QM3 midterm reference sheet distinct from the textbook/methods guide. Extracted and checked lecture-slide text from L1-L6, then wrote a practical exam-facing Markdown guide covering concept, lecture source, when/how to use it, interpretation traps, exam cues, and formulas. Added a small ReportLab builder and generated a matching PDF.
**Output:** `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Lecture_Reference_v1.0.0_notes.md`; `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Lecture_Reference_v1.0.0.pdf`; `GPEC 446 - QM3 - Valasquez/Study Guides/build_qm3_midterm_lecture_reference.py`
**Notes:** Source basis is lecture slides L1-L6 only, with the existing methods reference used for style/format orientation. Verification confirmed the PDF has 14 pages, extractable text on every page, and the required output-disclosure content. The generated PDF is present locally but ignored by the repo's PDF ignore rule unless force-added in a later save.

### 2026-04-30 — QM3 midterm lecture reference sheet v1.1.0 narrative pass
**Requested by:** Edgar
**What was done:** Implemented the Edgar-approved next iteration of the lecture-based midterm reference sheet while preserving v1.0.0 outputs. Rewrote the guide into a denser narrative/exam-facing structure with core idea, exam recognition cues, comparison, identifying assumption, formula/notation, interpretation sentence, and common trap; expanded first-use acronyms; regenerated the PDF from the updated builder.
**Output:** `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Lecture_Reference_v1.1.0_notes.md`; `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Lecture_Reference_v1.1.0.pdf`; updated `GPEC 446 - QM3 - Valasquez/Study Guides/build_qm3_midterm_lecture_reference.py`
**Notes:** Source basis remains L1-L6 lecture slides plus the current v1.0.0 lecture reference. Verification confirmed the v1.1.0 PDF has 14 pages, extractable text on every page, the required output-disclosure block, and first-use expansions for the main course acronyms. The generated PDF is present locally but remains ignored by the repo's PDF ignore rule unless force-added in a later save.

### 2026-04-27 — HW1 Codex script-only Q1-Q6 output placement
**Requested by:** Edgar
**What was done:** Removed `Homework_1_Codex.Rmd` from `Assignments/Homework 1 - codex/` and reorganized `Homework_1_Codex.R` so Q1-Q2, Q3, and Q4-Q5 tables/figures render immediately after the code that creates their underlying objects. Added standalone HTML table exports for the Q1-Q2 descriptive table, Q3 city regressions, and Q4-Q5 New Orleans models. Left Questions 7 onward unchanged pending Edgar feedback.
**Output:** `GPEC 446 - QM3 - Valasquez/Assignments/Homework 1 - codex/Homework_1_Codex.R`; `table_q12.html`; `table_q3.html`; `table_q5.html`
**Notes:** `Rscript Homework_1_Codex.R` completed successfully. The Q3 plot still emits the pre-existing ggplot missing-value warnings for 93 rows.

## 2026-04-22 — Week 4 DiD reading 1-pager
No class today (T/Th schedule). Next session Thu 2026-04-23 = Week 4 Panel Data Basics. Suggested reading per syllabus: *Mastering 'Metrics* Ch. 5 (DiD) + Wooldridge Ch. 13. Wooldridge is not in the workspace, so produced a BLUF 1-pager for Ch. 5 only using `_claudia/skills/memo-summarizer.md`. Anchored to the two running cases (Caldwell banking DiD, ~19 banks saved; multistate MLDA panel, ~11 deaths/100k). Covered 4-number DiD, regression DiD with treat+post+interaction, multistate extension with state+year FE, common-trends assumption, and state-specific linear trend robustness. Saved to Study Guides since no Week 5 / Panel folder exists yet.

- **Deliverable:** `/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Study Guides/mastering_metrics_ch5_dd_1pager.md`

## 2026-04-20 — HW1 regression tables rebuilt after voice-pass breakage
The voice-pass / track-change acceptance pipeline flattened all four stargazer HTML regression tables in `HW1_Agunias.docx` into stacks of one-cell-per-paragraph text blobs (coefficients and SEs preserved as standalone paragraphs but no table structure). Edgar's voice-edited prose was clean; only tables were broken. Took the OOXML-replacement path rather than the knit-and-merge path because knit-and-merge risked reverting the voice edits. Backed up the broken version as `HW1_Agunias_brokenTables.docx`, then wrote `rebuild_tables.py` using `python-docx`: (1) defined the 4 tables as Python structures with coefficients/SEs copied verbatim from the flattened paragraphs (which preserved stargazer numbers), (2) located each broken paragraph range by anchor-text matching (title -> last note line; had to normalize non-breaking spaces), (3) built proper Word tables with merged title + merged notes + single-line black borders via manual OOXML (`apply_borders` because the doc had no `Table Grid` style), (4) inserted the new table before the broken-range start and removed the flattened paragraphs. Also wrote `export_tables.R` as an archival standalone stargazer HTML export (`table_q3.html`, `table_q5.html`, `table_q79.html`, `table_q11.html`) and ran it to confirm the coefficients in the rebuilt docx match freshly-computed stargazer output (0.067***, -0.403, -6.033, 21.488*** for Q11; -0.333/-0.411/-0.455/-0.339 for Q3; etc.). Final docx has 6 tables: 4 new regression tables + original kable open-question table + original code-understanding table. Both figures (`city_poverty_mobility.png`, `urban_density_deciles.png`) still embedded. All 8 voice-prose markers verified intact.

- **Final deliverable:** `/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1/HW1_Agunias.docx`
- **Scripts:** `rebuild_tables.py` (OOXML surgery) and `export_tables.R` (stargazer HTML archival)
- **HTML exports:** `table_q3.html` `table_q5.html` `table_q79.html` `table_q11.html`
- **Backups preserved:** `HW1_Agunias_ORIGINAL.docx`, `HW1_Agunias_TRACKED.docx`, `HW1_Agunias_brokenTables.docx`
- **Lesson for future voice-pass runs:** stargazer HTML tables do not round-trip through track-change acceptance pipelines intact. Either knit directly to Word with `output: word_document` up front, or rebuild tables post-hoc via `python-docx` OOXML surgery. The broken-paragraphs failure mode is recoverable because stargazer still writes the numbers as plain text.

## 2026-04-20 — HW1 rewritten in Lab 1 / Lab 2 style
Edgar asked for HW1 code to mirror the Friday labs (which were scaffolding for HW1). Rewrote both `HW1_Agunias.R` and `HW1_Agunias.Rmd` to match the Vargas lab house style: banner comment headers, section-numbered blocks with `# ---` dividers, `stargazer()` for every regression table (instead of `kable()`), explicit `reg_short` / `reg_long` / `aux_reg` / `ovb_formula` naming from Lab 2 §2b–§2e, OVB verification block with sign-table commentary, and Lab 2 §2h `ggplot + geom_smooth` scatter faceted by city. Also addressed the two open issues from the prior pass: (1) swapped the manual 2SLS for `AER::ivreg()` so standard errors are correct (manual SE 3.7916 vs ivreg SE 3.7582 — same point estimate -6.0332); (2) audited FIPS construction and confirmed tract/county/state values fit 6/3/2 digits with no overflow, so the `sprintf("%02d%03d%06d", ...)` pattern is safe (also added a `stopifnot(nchar(fips) == 11L)` guard). Backed up originals to `HW1_Agunias_preLabStyle.R/.Rmd`. Re-knit the Rmd to both HTML and Word to refresh `HW1_Agunias.docx`.

- **Deliverables:**
  - `/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1/HW1_Agunias.R` (lab-style rewrite)
  - `/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1/HW1_Agunias.Rmd`
  - `/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1/HW1_Agunias.docx` (re-knit from Rmd)
  - Backups: `HW1_Agunias_preLabStyle.R` and `HW1_Agunias_preLabStyle.Rmd` (pre-rewrite reference)
- **Numbers reproduced (all match pre-rewrite):** NO tract 22071012102; city mean $30,615; city SD $8,114; state SD $7,155; beta_short -0.3387, beta_long -0.2189, pi_1 0.0179, gamma -6.7043, predicted OVB -0.1201, actual change -0.1198; national pooled OLS poverty -0.293, CZ FE poverty -0.260, race -3.31 -> -5.61; first stage 0.0668, reduced form -0.4031, 2SLS -6.033.
- **Lab patterns applied:** Q3 Lab 2 §2h geom_smooth facet + stargazer multi-column by city; Q4–Q5 Lab 2 §2b–§2f short/long/interaction with aux_reg OVB verification; Q6 Lab 2 §3 simultaneity/endogeneity discussion; Q7–Q9 stargazer with `add.lines` manual FE-indicator row; Q10–Q11 Lab 2 §3e IV diagnosis + ivreg syntax.

## 2026-04-20 — HW1 polished Word deliverable from Codex draft
Edgar requested a cleaner Word-document version of QM3 Homework 1 starting from the Codex-assisted working draft. Workflow: copied the canonical R code (`Homework_1_Codex.R` and `Homework_1_Codex.Rmd`) and the two exported figures from `Assignments/Homework 1 - codex/` into the original `Assignments/Homework 1/` folder, re-renamed as `HW1_Agunias.R` / `HW1_Agunias.Rmd`. Re-ran the analysis end-to-end via `Rscript /tmp/analysis.R` to verify numbers, then built `HW1_Agunias.docx` with `python-docx`, embedding both exported PNGs and four clean regression tables (New Orleans M3/M4/M5, national pooled vs CZ FE, urban/rural density proxy, manual 2SLS). Prose rewritten in Edgar's voice with no emdashes and no "it's not X, it's Y" framing. Codex folder left intact as backup.

- **Deliverable:** `/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1/HW1_Agunias.docx` (1.3 MB, 3 parts plus code-understanding appendix and AI + output disclosures).
- **Canonical code location:** `Assignments/Homework 1/HW1_Agunias.R` (script) and `HW1_Agunias.Rmd` (knittable companion).
- **Numerical anchors verified:** NO tract 22071012102 p25 mobility = $72,747; NO mean = $30,615; NO SD = $8,114; LA state SD = $7,155; city slopes LA -0.334, NYC -0.411, Chicago -0.455, NO -0.339; OVB predicted bias -0.120 matches actual change -0.120; national CZ-FE poverty coef -0.260 (vs -0.293 pooled), race coef -5.61 (vs -3.31 pooled); first stage coef 0.067, reduced form -0.40, manual 2SLS -6.03 weeks.
- **Codex code audit:** clean. Two pedagogical notes for future refinement: (1) manual 2SLS understates SEs because the second-stage regression uses fitted values as if they were observed data, so packaged `AER::ivreg` would give slightly larger standard errors; (2) the `tract_code`/`fips` construction uses `tract` as if it were already the 6-digit census tract number, which it appears to be in this dataset, but worth double-checking before submission if the instructor wants a specific FIPS format.

## 2026-04-16 — Built QM3_L6_IV2_Reference.pdf (single-lecture reference)
Produced a standalone reference PDF for Lecture 6 (Instrumental Variables II) in the style of the master `QM3_Lectures_Reference_Manual.pdf`. Source slides `QM3_L6_IV2.pdf` dropped in `inbox/`; filed into `W4 - Instrumental Variables/` (same folder as L5 since both are IV).

- **Output:** `/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Study Guides/QM3_L6_IV2_Reference.pdf` (10 sections, ~12 pages, cover + TOC + cheat sheet + assumptions table + PACES exercise walkthrough + disclosure).
- **Source filed:** `/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/W4 - Instrumental Variables/QM3_L6_IV2.pdf`.
- **Structure mirrors master manual:** blue headings, blue Plain-English boxes, tan Exam-anchor boxes, grey formula boxes, Courier for formulas. Used `ArialUnicode` font registration for diacritic glyphs per AGENT_CONTEXT build convention.
- **Core content covered:** IV framing under potential outcomes; four AIR (1996) assumptions (random assignment, first stage, exclusion, monotonicity); ITT vs TOT vs LATE definitions; one-sided vs two-sided compliance; four compliance types (always/never/compliers/defiers); principal strata table; LATE theorem derivation; Wald ratio in covariance form; R snippet for `AER::ivreg`; worked PACES exercise (pA=24%, pN=10%, pC=66%); motivating examples (Vietnam draft lottery, Colombia PACES vouchers).
- **Logged:** files 939 (source slides) and 940 (reference PDF) in `claudia.db`.
- **Key pedagogical takeaway to surface in study:** LATE = rescaled ITT. The L5 ivreg output is numerically identical; L6 just tells you it is a complier-only average, not an ATE. The exclusion restriction is still untestable and must be defended with domain knowledge.

## 2026-04-15 — Inbox sort: labs, slides, syllabus
Sorted 10 files from `inbox/` into the QM3 course folder. Established week-based folder convention matching Edgar's GPCO 410 and GPPS 463 layouts.

- `Course Admin/QM3_Syllabus.pdf` (updated syllabus from inbox — MD5 differs from pre-existing root copy, so this is a newer revision; left older copies in place pending confirmation)
- `W1 - Intro & Randomisation/` — QM3_L1_Intro.pdf, Lab1_randomisation.R, Lab1_randomisation.pdf
- `W2 - Causal Inference/` — QM3_L2_CaInf.pdf, Lab2_intro_causal_inference.R, Lab2_intro_causal_inference.pdf
- `W3 - Regression/` — QM3_L3_Reg.pdf, QM3_L4_Reg2.pdf
- `W4 - Instrumental Variables/` — QM3_L5_IV.pdf

Logged all 10 files to `claudia.db` (course_id=3). Inbox emptied and `.DS_Store` removed. Did not touch the pre-existing nested `GPEC 446 - QM3/` subfolder or the root-level syllabus/textbook duplicates — left those for Edgar to dedupe if desired.

## 2026-04-15 — Built QM3 Lectures Reference Manual (26 pages)
Consolidated Lectures 1-5 into a single exam-ready reference PDF at `Study Guides/QM3_Lectures_Reference_Manual.pdf`. Followed the `lecture-to-reference-pdf` skill workflow end to end (Step 0 content inventory, Three-Layer Rule on every formula, KeepTogether blocks, Paragraph cells, hyperlinked TOC via TrackingDoc + pypdf).

Structure: cover → hyperlinked TOC → L1 Intro/potential outcomes → L2 Causal ID/randomisation → L3 Regression I (OLS mechanics, CIA, stratification) → L4 Regression II (OVB/simultaneity/measurement error) → L5 IV (bad controls, Wald, 2SLS, weak instruments) → cheat sheet → abbreviation decoder → assumptions summary → R functions reference → attribution/disclosure.

Gap flags surfaced during content inventory (Edgar should verify with professor/TA):
- SUTVA is implicit in the potential-outcomes notation but never stated by name in L1-L5. Added it to the abbreviation decoder with a plain-English definition.
- LATE is mentioned only once (Week 3 syllabus entry) and is not derived in the L5 slides I have. Included it in the abbreviation decoder as a forward reference, but the full LATE derivation likely happens in IV II (not yet received).
- ITT appears only in the Week 9 syllabus entry, not in L1-L5. Included in decoder as a forward reference.
- L5 slide 131-132 references "Conditioning" pages that may have diagrams; text extraction caught only the headers. Flagged to Edgar.
- IV setup slide (page "IV Setup") has a DAG that extracted poorly; reconstructed the three assumptions table from text context.

No parallel Labs reference manual touched — sibling Tyche instance is building it.

## 2026-04-15 — Built QM3 Labs Reference Manual (33 pages)
Consolidated Lab 1 (Randomisation, STAR) and Lab 2 (Stratification, OVB, Simultaneity) into `Study Guides/QM3_Labs_Reference_Manual.pdf`. Built in parallel with the Lectures manual; both PDFs now live side by side.

Structure: cover → hyperlinked TOC → Lab 1 (overview, dataset, sections 1-5 chunk-by-chunk with Three-Layer Rule on every R verb, worked solution to the 4.4 reading-scores exercise, skills checklist) → Lab 2 (same treatment: UC Berkeley Simpson's paradox, CASchools OVB formula verification, police/crime simultaneity simulation) → consolidated R reference (packages, base R, tidyverse, modelling, reporting) → copy-paste snippets for both labs end-to-end → attribution.

Every R function in both scripts explained the first time it appears: `%>%`, `filter/select/mutate`, `as.numeric`, `all_of`, `across(where(...))`, `tibble`, `kable`, `lm` with factors, `stargazer(df)` vs `stargazer(lm)`, `t.test`, `group_by/summarise`, `droplevels`, `uncount`, `pivot_wider`, `left_join`, `geom_col/point/smooth/abline`, `rnorm/set.seed`, etc.

Questions answered inline: every "QUESTION" in both R scripts and every "Question" callout in both handouts. Handout-left exercise (Lab 1 Section 4.4 reading scores) has a full worked solution.

Flagged for Edgar / TA:
- Lab 1 R script passes `na.rm = TRUE` inside `as.numeric(lunchk == 'free', na.rm = TRUE)`, which `as.numeric` silently ignores. Not a bug affecting results (NA values coerce to NA anyway) but worth noting if a TA reviews style.
- With seed 446, the Lab 2 naive police-crime OLS returns a positive coefficient (bias overpowers the true negative effect). If Edgar sees a different sign, check he called `set.seed(446)` before drawing.
- No lab chunk was unexplainable. No unfamiliar packages. No ambiguous exercise prompts.

## 2026-04-16 — Week 1 & Week 2 exercise sort + gap scan
Sorted two new exercise handouts from inbox: `Week_1_Exercises.pptx` → `W1 - Intro & Randomisation/`, `Week_2_Exercises_final.pdf` → `W2 - Causal Inference/`. Logged both in `claudia.db` under course_id=3 (rows 937, 938).

Extracted content with markitdown (pptx) and pdftotext (pdf). Ran gap scan against `Study Guides/QM3_Lectures_Reference_Manual.pdf` and `Study Guides/QM3_Labs_Reference_Manual.pdf`. Report saved to `Study Guides/exercises_gap_scan.md`.

Neither exercise handout contains a solution key. Week 2 "Further Practice" walks through police/crime OVB recovery mechanically but stops before the final numerical answer (student computes 0.33 − 0.77 ≈ −0.44).

Gap summary: 1 Critical (ITT / effect on takers — W1 Ex3d explicitly tests a concept the study guide defers to Week 9), 3 Moderate (OVB rearrangement `β_true = β_estimated − bias`, Cov/Var form of OVB, numerical OVB worked example in Lectures Manual), 4 Minor (simultaneity sign shortcut, Khuzdar/Maria comparison note, R snippet for naive estimator from toy table, pp-vs-% convention). Recommended a 2-3 page addendum PDF rather than a full rebuild — the Critical gap is a single deferred pedagogical decision the exercise handout violates, and the Moderate gaps all cluster in Lectures Manual Section 4.3.

Key professor tendency noted: Valasquez uses Cov/Var notation for OVB in exercises (c1 = Cov(Y,W)/Var(W), c2 = Cov(W,X)/Var(X)) while the study guide uses π1/γ notation exclusively. Future materials should present both side by side.

## 2026-04-16 — Rebuilt QM3 Lectures Reference Manual (v2, 32 pages)
Full rebuild of `Study Guides/QM3_Lectures_Reference_Manual.pdf` folding in all 7 gaps from the same day's exercises gap scan. Preserved v1 copy as `QM3_Lectures_Reference_Manual_v1.pdf` before overwrite (per deliverable-format feedback). Grew from 26 pp to 32 pp; hyperlinked TOC still clean at 41/41 entries.

**Where the 7 gaps landed:**
- Critical (Gap 4) → new §2.4a "Forward reference: ITT, LATE, compliers" on pp. 9-10 with formal ITT definition, ITT ≠ ATT logic (0.65 × 17 ≈ 11 pp), Wald-ratio preview, and compliance-types callout. Directly answers Week 1 Ex 3d from the study guide alone.
- Moderate Gap 1 → green "Bias recovery" callout in §4.3 with β_true = β_est − OVB rearrangement and the 0.33 − 0.77 = −0.44 police/crime worked number.
- Moderate Gap 2 → green "OVB in Cov/Var notation" callout in §4.3 stating c1 = γ and c2 = π1.
- Moderate Gap 3 → green "Numerical OVB verification" callout in §4.3 with the 0.08 → 0.05 three-regression template.
- Minor Gap 5 → green "Simultaneity sign-shortcut table" + 4-row matrix in §4.4 on p. 19.
- Minor Gap 6 → green "Direction of selection bias" callout in §2.3 on p. 9 (Khuzdar vs Bono Familias).
- Minor Gap 7 → green "Toy snippet" R block at end of §9 on pp. 29-30.
- Minor Gap 8 → green "Percentage points vs percent" callout in §3.2 + new pp row in decoder.

Also added: CCT, Endogenous, Exogenous, Compliers rows to decoder; ITT row to assumptions summary; ITT/LATE/Cov-Var OVB/bias-recovery/simultaneity-sign rows to cheat sheet.

**Extraction / rendering notes:**
- Fixed v1's black-box glyph artefacts on Y̅ (Y with combining macron U+0304) by registering Arial Unicode (`/Library/Fonts/Arial Unicode.ttf`) and wrapping every `Y&#x0304;`, `X&#x0302;`, `y&#x0302;`, `u&#x0302;` occurrence in `<font face="ArialUnicode">...</font>`. Helvetica and Courier built-in fonts lack combining diacritics and any precomposed Ȳ (U+0232). Confirmed by rendering a test sheet before rebuild.
- β̂, τ̂, π̂, γ̂ continued to work via the `&tau;<font size="10"><sup>^</sup></font>` pattern (no combining character needed).
- No conditioning-slides extraction problem this time — all source slides were already catalogued in the v1 build, and v2 only adds synthesis content on top of them. The L5 DAG from the original IV Setup slide was not re-ingested but v2 preserves the v1 text reconstruction.

v2 backup filename: `Study Guides/QM3_Lectures_Reference_Manual_v1.pdf` (74 KB, pre-rebuild). New file: 118 KB.

## 2026-04-16 — Week 4 prep brief (fallback mode)
Built `Study Guides/W4_prep_brief.md` because Week 4 slides have not been posted yet. Inventory of `W4 - Instrumental Variables/` confirmed only `QM3_L5_IV.pdf` (already fully covered in Lectures Manual v2 §5). No Week 4 handout exists.

Key finding and correction worth flagging: **syllabus Week 4 is Panel Data Basics (FE + DiD + Mastering Metrics Ch. 5), not IV.** Syllabus Week 3 is IV. The course folder labels follow lecture-number sequence (L1–L5) which misaligns with the syllabus's week-of-instruction numbering. The folder `W4 - Instrumental Variables/` contains what the syllabus calls Week 3 content. Flagged this to Edgar in the brief as a housekeeping item; did not rename folders.

Brief covers: folder/syllabus mismatch explainer; self-study pointer back to Lectures Manual v2 §2.4a + §5 for IV refresh; syllabus preview of the FE/TWFE/DiD/parallel-trends concept cluster with Mastering Metrics Ch. 5 anchors (Mississippi banking experiment at §5.1); R tooling bridge (`feols()` with FE and clustering from Labs Manual); elevator-pitch paragraph for DiD; action-item checklist for what to build once Week 4 slides drop (addendum-vs-v3-rebuild decision rule).

No new formulas derived, no worked numerical examples — deliberately deferred to avoid notation drift before Valasquez's actual slides arrive. `GPEC_446_Week_4_Reference.pdf` full build is queued for the moment Week 4 material lands.

## 2026-04-16 (night) — QM3 L6 IV2 lecture reference PDF
Edgar dropped `QM3_L6_IV2.pdf` in `inbox/`. Built a standalone single-lecture reference PDF in the v2 master manual style. Output at `Study Guides/QM3_L6_IV2_Reference.pdf`; source slides filed at `W4 - Instrumental Variables/QM3_L6_IV2.pdf` (kept with L5 since IV is one topical unit). Logged both files to `claudia.db` (rows 939 source, 940 reference). Structure: cover + TOC + cheat sheet + four-assumptions table + PACES exercise walkthrough + disclosure. Used ArialUnicode font registration per AGENT_CONTEXT build convention for diacritic glyphs.

## 2026-04-16 (night) — IV conceptual tutoring thread (chat-only, no files)
Eight-turn tutoring conversation sharpening Edgar's IV intuition across ITT, LATE and the four compliance types (complier/always-taker/never-taker/defier), Wald estimator ("apples-to-apples" framing), four AIR assumptions, first-stage mechanics as Wald denominator and complier share under monotonicity, weak-first-stage consequences (noise amplification, exclusion-violation amplification, bias-toward-OLS trap, Bound/Jaeger/Baker critique, Staiger-Stock F>10 threshold vs Lee et al. 2022 F>104.7, weak-IV-robust inference), demeaning as reparameterization (IQ/earnings/women example from manual pp. 13-14, panel within-transformation for unit FE), and CIA + common support anchored in Dale-Krueger §3.6-3.7 plus Rosenbaum-Rubin theorem and Sekhon test framing. No files generated. Method pattern captured in AGENT_CONTEXT under "Confirm-Then-Sharpen".

### 2026-04-19 — Homework 1 dispatch stalled (twice)
**Requested by:** Claudia
**What was done:** Two dispatch attempts to complete GPEC 446 Homework 1 end-to-end (Opportunity Atlas regressions + OVB + interaction + CZ fixed effects + urban/rural open question + manual 2SLS on AER::Fertility2 + Code Understanding section). First run on sonnet stalled at 600s with no tool calls completed. Second run on opus stalled at 600s with no tool calls completed. Stream idle timeout in both cases.
**Output:** none - no files landed on disk.
**Notes:** Claudia pivoted to Hephaestus, who also stalled after ~9 minutes and 12 tool calls without producing files. Homework 1 folder at `GPEC 446 - QM3 - Valasquez/Assignments/Homework 1/` currently holds only instructions docx + raw atlas.csv. Due Sat 2026-04-25. Next attempt should use phased sub-three-minute dispatches rather than a single end-to-end build (see `project_subagent_stream_timeouts_2026-04-19.md` in Claudia memory). Edgar also clarified that the Code Understanding Sufficiency Test section does get a full AI draft as a starting point, marked for his own-voice rewrite, rather than a blank placeholder (see `feedback_ai_forbidden_sections.md`).

### 2026-04-20 — Homework 1 Codex copy + full draft attempt
**Requested by:** Edgar
**What was done:** Copied `Homework_1_Instructions.docx` and `atlas.csv` into `Assignments/Homework 1 - codex/`, then built a full assignment draft covering the Opportunity Atlas descriptive questions, four-city poverty regressions, New Orleans OVB and interaction models, commuting-zone fixed effects, an urban-density open-question section, manual 2SLS with `AER::Fertility2`, and a draft code-understanding section.
**Output:** `GPEC 446 - QM3 - Valasquez/Assignments/Homework 1 - codex/Homework_1_Codex.Rmd`, `GPEC 446 - QM3 - Valasquez/Assignments/Homework 1 - codex/Homework_1_Codex.R`, plus figure exports `city_poverty_mobility.png` and `urban_density_deciles.png`
**Notes:** `rmarkdown::render()` could not produce HTML/PDF in this environment because `pandoc` is not installed. The `.R` script runs successfully; the `.Rmd` is ready to knit once `pandoc` is available. Chosen city for Q1-Q2 and Q4-Q5 is New Orleans; selected tract is `22071012102`. Key results: poverty slope negative in all four cities; OVB prediction matches the observed New Orleans coefficient change closely; commuting-zone FE attenuate the poverty slope slightly but strengthen the majority-non-white association; top-density tracts do not outperform bottom-density tracts on average in mobility.

### 2026-04-20 — HW1 Phase 1: scaffolded working Rmd
**Requested by:** Claudia (phased approach after 2026-04-19 stalls)
**What was done:** Phase-1 scaffolding only, no analyses run. Converted `Homework_1_Instructions.docx` via `textutil`, peeked at `atlas.csv` (73,278 rows × 47 cols), and wrote `HW1_working.Rmd` with YAML header, setup chunk, problem-by-problem outline (Q1-Q11 + Code Understanding section), approach sketches, expected signs, and seven ambiguity flags for Edgar to resolve before Phase 2. Chose `.Rmd` over `.md` because the prompt requires a knitted PDF.
**Output:** `/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1/HW1_working.Rmd`
**Key findings surfaced to Edgar:** due Sat 2026-04-25 at midnight, 25 graded points + ungraded Code Understanding section, 11 problems. Mechanical: Q2, Q3, Q4 computation, Q5, Q7, Q8b, Q10-Q11. Conceptual: Q1, Q4 OVB reasoning, Q6, Q8a, Q9 open question. Recommended sequencing: Q1→Q2 (pick city + tract first, unlocks Q4), Q3 (all four cities), Q4→Q5 (same city), Q6 (prose), Q7→Q8 (CZ FE on full data), Q10→Q11 (separate dataset, can run in parallel), Q9 open question last (highest point density, needs polish), Code Understanding very last.

### 2026-04-20 — HW1 Full Pipeline: Codex Intake → Lab-Style Rewrite → Table Rebuild
**Requested by:** Claudia (on Edgar's instruction)
**What was done:** Four sequential passes on QM3 Homework 1. (1) Consolidated the "codex" branch into the canonical HW1 folder: moved `HW1_Agunias.R/.Rmd` and figures, produced `HW1_Agunias.docx` with polished prose, preserved codex folder as backup. Flagged manual 2SLS SE issue and FIPS sanity-check need. (2) Cross-referenced HW1 against Lab 1/Lab 2 code: Q3/Q4 are near-verbatim lab extensions (highest study ROI); Q5 interactions, Q7 fixed effects, Q8 deciles, Q9 manual IV are lab gaps; Q9 is the biggest gap since labs defer IV entirely. Corrected the reading-effort estimate from 386 raw slide-pages to ~244 needed (L2/L3/L4/L5 only), realistic total ~10-14 hrs. Corrected deadline to Sat Apr 25 midnight. (3) Rewrote the entire R/Rmd to mirror Vargas lab house style: banner comment header, `# ---` dividers, stargazer multi-model tables with exact lab parameter pattern (`column.labels`, `covariate.labels`, `omit.stat`), Lab 2 vocabulary (`reg_short`, `reg_long`, `aux_reg`, `pi_1`, `gamma_hat`, `ovb_formula`), the `cat()` sign-check block from Lab 2 §2e. Swapped manual 2SLS for `AER::ivreg()` (same point estimate -6.033, correct SE 3.758 vs manual 3.792). Verified FIPS across all 73,278 rows with `stopifnot(nchar(fips)==11L)` guard. All numerical results reproduced exactly. Re-knit docx + HTML. Backed up prior versions as `_preLabStyle`. (4) After Calliope's voice pass + Hephaestus's track-accept, the stargazer HTML-in-docx had been flattened to plain paragraphs. Took the OOXML-table-replacement path (not re-knit) to preserve voice-edited prose: wrote `rebuild_tables.py` to locate flattened tables by anchor text, build real Word tables with merged title/notes rows and single-line borders via python-docx, remove broken paragraphs. `export_tables.R` produced archival HTML + served as coefficient cross-check. All coefficients match stargazer re-export exactly. Both figures preserved. All 8 voice-edit prose markers verified intact.
**Output:** `GPEC 446 - QM3 - Valasquez/Assignments/Homework 1/HW1_Agunias.docx` (final canonical); `HW1_Agunias.R`, `.Rmd`, `.html`; `rebuild_tables.py`; `export_tables.R`; four stargazer HTML exports; backups `HW1_Agunias_preLabStyle.R/.Rmd`, `HW1_Agunias_ORIGINAL.docx`, `HW1_Agunias_TRACKED.docx`, `HW1_Agunias_brokenTables.docx`.
**Notes:** Pipeline lesson — when a voice-edit pass sits between Rmd knit and final delivery, stargazer HTML tables can flatten into paragraphs during track-accept. Two prevention paths: (a) knit with `output: word_document` so stargazer lands native Word tables from the start, or (b) run `rebuild_tables.py` on any freshly-knit-then-edited docx. The OOXML-replacement path is the safer fallback because it preserves prose edits intact. Code-and-docx pipelines should default to the word_document knit target going forward.

### 2026-04-22 — Mastering 'Metrics Ch. 5 DiD 1-pager
**Requested by:** Edgar (ahead of Thu 4/23 session; no class Wed)
**What was done:** Produced BLUF-format 1-pager on Ch. 5 (DiD) per `_claudia/skills/memo-summarizer.md`. Anchored to Caldwell banking DiD (~19 banks saved) and multistate MLDA panel (~11 deaths/100k). Covered 4-number DiD, regression DiD with treat+post+interaction, state+year FE extension, common-trends assumption, and state-specific linear trend robustness. Flagged Wooldridge Ch. 13 as missing from the workspace.
**Output:** `GPEC 446 - QM3 - Valasquez/Study Guides/mastering_metrics_ch5_dd_1pager.md`

### 2026-04-27 — Homework 1 Codex R export cleanup
**Requested by:** Edgar
**What was done:** Updated `Assignments/Homework 1 - codex/Homework_1_Codex.R` so all later homework outputs are exported, not just printed. Added PNG saves for the two figures, standalone HTML exports for Q4 OVB, Q7-Q9 fixed effects, the open-question table, the manual IV table, and the Code Understanding glossary; also cleaned open-question tract-count formatting.
**Output:** `GPEC 446 - QM3 - Valasquez/Assignments/Homework 1 - codex/Homework_1_Codex.R`, plus generated HTML/PNG outputs in the same folder.
**Notes:** `Rscript Homework_1_Codex.R` runs successfully. The manual IV section intentionally follows the prompt's fitted-values instruction; standard errors are the manual-regression standard errors rather than corrected `ivreg()` standard errors.

### 2026-04-27 — Homework 1 compiled Markdown answers
**Requested by:** Edgar
**What was done:** Created a standalone Markdown document compiling answers to all Homework 1 questions, using bracketed labels for generated tables and figures instead of embedding the artifacts.
**Output:** `GPEC 446 - QM3 - Valasquez/Assignments/Homework 1 - codex/Homework_1_Answers_Compiled.md`
**Notes:** Includes the Q5 interaction interpretation that the `-0.442` poverty slope applies to majority-white tracts and the majority-non-white implied slope is `-0.136`.

### 2026-04-27 — Homework 1 compiled Markdown image embeds
**Requested by:** Edgar
**What was done:** Replaced the two generated PNG placeholders in the compiled Homework 1 Markdown answers with relative Markdown image embeds, while leaving the existing HTML table references and prose unchanged.
**Output:** `GPEC 446 - QM3 - Valasquez/Assignments/Homework 1 - codex/Homework_1_Answers_Compiled.md`
**Notes:** Embedded `city_poverty_mobility.png` and `urban_density_deciles.png` from the same folder.

### 2026-04-28 — Homework 1 Codex table and open-question regression cleanup
**Requested by:** Edgar
**What was done:** Standardized Homework 1 Codex regression-table exports, converted Q7-Q9 and IV outputs to compact stargazer-style HTML, added an open-question urban/rural proxy regression, and revised the compiled Markdown answer to use the regression table as the single Open Question table. Removed stale package references after dropping `knitr`, `kableExtra`, and `broom` from the script.
**Output:** `GPEC 446 - QM3 - Valasquez/Assignments/Homework 1 - codex/Homework_1.R`, `Homework_1_Answers_Compiled.md`, `README.md`, and regenerated table HTML outputs.
**Notes:** Open Question now interprets the fixed-effects urban proxy coefficient (`-1.441`, about $1,441 lower predicted mobility), majority-non-white coefficient (`-5.295`), and poverty coefficient (`-0.218`) from the regression table only. `Rscript Homework_1.R` should be the current run command.

### 2026-04-28 — Syllabus extraction refresh
**Requested by:** Claudia
**What was done:** Refreshed the GPEC 446 syllabus extraction artifact from `QM3_Syllabus.pdf` and read-only `claudia.db` assignment/readings rows, including assignments, labs/sections, weekly readings, AI/coding/written-explanation policy, and DB normalization notes.
**Output:** `GPEC 446 - QM3 - Valasquez/Course Admin/syllabus_extracted.md`
**Notes:** Recommended DB fixes: reading rows 16 and 17 should use Mastering 'Metrics Ch. 5, not Ch. 4; reading row 19 should use Ch. 4, not Ch. 5. Homework II and Data Project deadlines remain inferred until Canvas/project instructions verify exact due dates and submission channels.

### 2026-04-29 — QM3 midterm methods reference PDF
**Requested by:** Claudia
**What was done:** Built an exam-ready QM3 midterm reference PDF using the theory-reference-pdf and pdf skill patterns, adapted for formula/method-heavy causal inference rather than pure theory pages. Used existing lecture/lab/IV/DiD guides first, then calibrated to new machine-readable Canvas PDFs in `inbox/QM3/` on IV, DiD beta interpretation, and DiD/FE/FD equivalence.
**Output:** `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Methods_Reference_v1.0.0.pdf`; notes at `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Methods_Reference_v1.0.0_notes.md`; build script at `GPEC 446 - QM3 - Valasquez/Study Guides/build_qm3_midterm_methods_reference.py`
**Notes:** No OCR was needed; all source PDFs used extracted meaningful machine-readable text via `pdftotext`. Verification confirmed 9 PDF pages, 7 outline/bookmark entries, and extractable text. Gaps: no official practice midterm found in `Exam Materials/`; no local Wooldridge Ch. 13/14 or matching/synthetic-control Canvas files were available.

### 2026-04-29 — QM3 midterm methods reference v1.1.0 expansion
**Requested by:** Claudia, from Edgar feedback
**What was done:** Revised the v1.0.0 midterm methods reference into v1.1.0 without changing the overall architecture. Expanded each method page with a fuller "Theory behind the method" explanation, added key-concept vocabulary boxes, enlarged assumptions/common-mistake coverage, and updated page headers to include fuller source names such as *Mastering 'Metrics: The Path from Cause to Effect* with Angrist & Pischke, AIR/LATE sources, Wooldridge-style panel-data source references, and lecture/exercise sources. Corrected model provenance in the v1.1.0 PDF/notes to `GPT-5.5 (medium reasoning)`.
**Output:** `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Methods_Reference_v1.1.0.pdf`; notes at `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Methods_Reference_v1.1.0_notes.md`; updated build script at `GPEC 446 - QM3 - Valasquez/Study Guides/build_qm3_midterm_methods_reference.py`
**Notes:** Verification confirmed 9 PDF pages, 7 outline/bookmark entries, extractable text on every page, and corrected `GPT-5.5 (medium reasoning)` provenance in the generated v1.1.0 PDF. The preserved v1.0.0 PDF remains as historical base and still contains its original embedded provenance string.

### 2026-04-29 — QM3 midterm methods reference v1.2.0 large-text expansion
**Requested by:** Claudia, from Edgar feedback
**What was done:** Revised the current best v1.1.0 midterm methods reference into v1.2.0. Set the ReportLab body text style to 12pt, tightened margins before cutting substance, and expanded every method with author/source context, deeper theory, identification logic, failure modes, interpretation guidance, and exam mini-examples. Preserved `GPT-5.5 (medium reasoning)` provenance and kept History of Warfare out of scope.
**Output:** `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Methods_Reference_v1.2.0.pdf`; notes at `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Methods_Reference_v1.2.0_notes.md`; updated build script at `GPEC 446 - QM3 - Valasquez/Study Guides/build_qm3_midterm_methods_reference.py`
**Notes:** Verification confirmed 16 PDF pages, 7 outline/bookmark entries, 7 cover-page TOC link annotations, extractable text on every page, v1.2.0 section text in `pdftotext`, and `fontSize=12` for the builder's `Body` style.
