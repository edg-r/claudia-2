# Tyche — GPEC 446 Task Log

Record of major completed tasks. Read to avoid duplicate work.

<!-- No entries yet. Append new tasks below this line. -->

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
