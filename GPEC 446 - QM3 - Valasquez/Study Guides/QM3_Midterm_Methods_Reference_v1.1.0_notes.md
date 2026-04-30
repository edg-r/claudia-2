# QM3 Midterm Methods Reference v1.1.0 — Source Notes

## Deliverable

- PDF: `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Methods_Reference_v1.1.0.pdf`
- Build script: `GPEC 446 - QM3 - Valasquez/Study Guides/build_qm3_midterm_methods_reference.py`
- Base version preserved: `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Methods_Reference_v1.0.0.pdf`

## Revision Scope

This is a minor-version revision of the v1.0.0 QM3 midterm methods reference. It keeps the same architecture and method order, but expands the method pages so each one more fully explains the theory behind the estimator or research design.

Changes from v1.0.0:

- Added a dedicated "Theory behind the method" paragraph to each method page.
- Added fuller "Key Concepts" vocabulary boxes alongside assumptions.
- Expanded assumptions, common mistakes, and quick-check prompts.
- Updated the header/source area on each method page to include fuller source names, including *Mastering 'Metrics: The Path from Cause to Effect*, Angrist & Pischke, AIR/LATE sources, Wooldridge-style panel-data source references where applicable, and named lecture/exercise sources.
- Corrected model provenance in the v1.1.0 PDF and notes to `GPT-5.5 (medium reasoning)`.

## Sources Used

Existing generated guides used first:

- `Study Guides/QM3_Lectures_Reference_Manual.pdf` — used for potential outcomes, selection bias, OLS, controls, interactions, OVB, simultaneity, IV, 2SLS, weak instruments, and assumption framing.
- `Study Guides/QM3_Labs_Reference_Manual.pdf` — used for lab-style R/concept links, balance/difference-in-means, OVB verification, simultaneity simulation, and practical interpretation patterns.
- `Study Guides/QM3_L6_IV2_Reference.pdf` — used for ITT, compliance types, LATE, AIR assumptions, Wald ratio, and `ivreg()` inference warnings.
- `Study Guides/mastering_metrics_ch5_dd_1pager.md` — used for DiD, common trends, state/year FE, and multistate panel framing.
- `Study Guides/exercises_gap_scan.md` — used for known pre-midterm gaps and professor-preferred exercise notation, especially Cov/Var OVB, bias recovery, ITT/take-up, and percentage-point conventions.
- `Course Admin/syllabus_extracted.md` and `Course Admin/QM3_Syllabus.pdf` — used to confirm midterm timing, course emphasis, and Week 3-6 topic ordering.
- Tyche memory files `GPEC 446 - QM3 - Valasquez/_agent/AGENT_CONTEXT.md` and `FEEDBACK.md` — used for course arc, professor tendencies, and ReportLab notation cautions.

New Canvas/inbox calibration files retained from v1.0.0:

- `inbox/QM3/week3_IV_exercise_v2.pdf`
- `inbox/QM3/Interpreting all β's in DiD.pdf`
- `inbox/QM3/Week 6 Exercises DiD FE FD.pdf`

## Gaps / Caveats

- No official practice midterm was present in `Exam Materials/`; depth is calibrated from in-class exercises and syllabus topic order.
- Wooldridge Ch. 13/14 files were not present locally, so fixed-effects/DiD coverage relies on the syllabus, generated study guides, Mastering 'Metrics Ch. 5 one-pager, and Canvas exercises.
- Matching/synthetic control appears as Week 6 on the syllabus, but no new matching/synthetic-control Canvas files were available in `inbox/QM3/`. The PDF does not add a full matching/synthetic-control page.
- The preserved v1.0.0 PDF still contains its historical embedded provenance string. The corrected provenance is applied in v1.1.0 and in these notes.

## Verification

- `python3 Study Guides/build_qm3_midterm_methods_reference.py` generated the v1.1.0 PDF successfully.
- `pypdf` verification confirmed the generated PDF has 9 pages and 7 outline/bookmark entries.
- `pypdf` text extraction confirmed all method pages contain extractable text, with roughly 2,700-3,100 extracted characters on each expanded method page.
- `pdftotext` on the generated PDF confirmed expanded sections such as "Theory behind the method," full source/header strings, references, and the corrected `GPT-5.5 (medium reasoning)` provenance.

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5.5 (medium reasoning)
Sources: QM3 generated reference manuals, QM3 syllabus extraction, Tyche memory, machine-readable Canvas PDFs in `inbox/QM3/`, and v1.0.0 midterm methods reference artifacts
Agent: Tyche
---
