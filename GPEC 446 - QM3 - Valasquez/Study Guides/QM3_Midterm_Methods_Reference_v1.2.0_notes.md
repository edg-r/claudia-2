# QM3 Midterm Methods Reference v1.2.0 - Source Notes

## Deliverable

- PDF: `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Methods_Reference_v1.2.0.pdf`
- Build script: `GPEC 446 - QM3 - Valasquez/Study Guides/build_qm3_midterm_methods_reference.py`
- Base version preserved: `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Methods_Reference_v1.1.0.pdf`

## Revision Scope

This is a minor-version revision of the v1.1.0 QM3 midterm methods reference. It keeps the same method order and core architecture, but expands the method pages and increases readability.

Changes from v1.1.0:

- Updated the builder output target to `QM3_Midterm_Methods_Reference_v1.2.0.pdf`.
- Set the main `Body` paragraph style to 12pt in the ReportLab builder.
- Widened the usable page area by tightening margins before cutting substance.
- Added an `Author/source context` block to every method page so Edgar can place Angrist & Pischke, Rubin-style potential outcomes, AIR/LATE, Wooldridge-style panel tools, and the course exercise environment in time and method context.
- Added fuller `Identification logic`, `Failure modes`, and `Interpretation` blocks for every method.
- Added `Exam mini-example` blocks so the larger-font continuation pages contain useful applied practice rather than sparse carryover material.
- Preserved the model provenance as `GPT-5.5 (medium reasoning)`.
- Kept History of Warfare out of scope.

## Sources Used

Existing generated guides and course artifacts used as the source base:

- `Study Guides/QM3_Midterm_Methods_Reference_v1.1.0.pdf` and v1.1.0 builder.
- `Study Guides/QM3_Lectures_Reference_Manual.pdf` - potential outcomes, selection bias, OLS, controls, interactions, OVB, simultaneity, IV, 2SLS, weak instruments, and assumption framing.
- `Study Guides/QM3_Labs_Reference_Manual.pdf` - lab-style R/concept links, OVB verification, simultaneity simulation, and practical interpretation patterns.
- `Study Guides/QM3_L6_IV2_Reference.pdf` - ITT, compliance types, LATE, AIR assumptions, Wald ratio, and `ivreg()` inference warnings.
- `Study Guides/mastering_metrics_ch5_dd_1pager.md` - DiD, common trends, state/year FE, and panel framing.
- `Study Guides/exercises_gap_scan.md` - professor-preferred exercise notation, especially Cov/Var OVB, bias recovery, ITT/take-up, and percentage-point conventions.
- `Course Admin/syllabus_extracted.md` and `Course Admin/QM3_Syllabus.pdf` - midterm timing, course emphasis, and Week 3-6 topic ordering.
- Tyche memory files `GPEC 446 - QM3 - Valasquez/_agent/AGENT_CONTEXT.md` and `FEEDBACK.md` - course arc, professor tendencies, and ReportLab notation cautions.
- Canvas/inbox calibration files retained from prior versions:
  - `inbox/QM3/week3_IV_exercise_v2.pdf`
  - `inbox/QM3/Interpreting all beta's in DiD.pdf`
  - `inbox/QM3/Week 6 Exercises DiD FE FD.pdf`

## Gaps / Caveats

- No official practice midterm was present in `Exam Materials/`; depth remains calibrated from in-class exercises and syllabus topic order.
- Wooldridge Ch. 13/14 files were not present locally, so fixed-effects/DiD coverage relies on the syllabus, generated study guides, Mastering 'Metrics Ch. 5 one-pager, and Canvas exercises.
- Matching/synthetic control appears as Week 6 on the syllabus, but no new matching/synthetic-control Canvas files were available in `inbox/QM3/`. The PDF does not add a full matching/synthetic-control page.
- The larger 12pt body text means several methods now span two pages. The builder keeps method starts clean with page breaks and fills continuation pages with concept boxes and exam mini-examples.

## Verification

- `python3 Study Guides/build_qm3_midterm_methods_reference.py` generated the v1.2.0 PDF successfully.
- `pypdf` verification confirmed the generated PDF has 16 pages and 7 outline/bookmark entries.
- `pypdf` verification confirmed the cover page contains 7 link annotations for the hyperlinked table of contents.
- `pypdf` text extraction confirmed every page has extractable text.
- `pdftotext` confirmed the generated PDF includes `Version 1.2.0`, `Author/source context`, `Identification logic`, `Failure modes`, `Interpretation`, `Exam mini-example`, and `GPT-5.5 (medium reasoning)`.
- `rg` verification of the builder confirmed `Body` style uses `fontSize=12` and the output target is `QM3_Midterm_Methods_Reference_v1.2.0.pdf`.

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5.5 (medium reasoning)
Sources: QM3 generated reference manuals, QM3 syllabus extraction, Tyche memory, machine-readable Canvas PDFs in `inbox/QM3/`, and v1.1.0 midterm methods reference artifacts
Agent: Tyche
---
