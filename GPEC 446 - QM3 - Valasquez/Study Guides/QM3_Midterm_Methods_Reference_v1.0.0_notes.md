# QM3 Midterm Methods Reference v1.0.0 — Source Notes

## Deliverable

- PDF: `GPEC 446 - QM3 - Valasquez/Study Guides/QM3_Midterm_Methods_Reference_v1.0.0.pdf`
- Build script: `GPEC 446 - QM3 - Valasquez/Study Guides/build_qm3_midterm_methods_reference.py`

## Scope Decision

The requested skill was `_claudia/skills/theory-reference-pdf.md`, used alongside `_claudia/skills/pdf.md`. Because QM3 is formula/method-heavy, I adapted the theory-reference structure rather than forcing one-page "theory" pages. Each page is a method-reference page with:

- situation anchor
- core formula / estimator
- exam moves
- assumptions to state
- common mistakes

This preserves the exam-ready navigation, TOC, bookmarks, and disclosure requirements while matching the course's causal-inference and econometrics style.

## Sources Used

Existing generated guides used first:

- `Study Guides/QM3_Lectures_Reference_Manual.pdf` — machine-readable; extracted with `pdftotext`; used for potential outcomes, selection bias, OLS, OVB, simultaneity, IV, 2SLS, weak instruments, and abbreviation/assumption framing.
- `Study Guides/QM3_Labs_Reference_Manual.pdf` — machine-readable; extracted with `pdftotext`; used for lab-style R/concept links, balance/difference-in-means, OVB verification, simultaneity simulation, and practical interpretation patterns.
- `Study Guides/QM3_L6_IV2_Reference.pdf` — machine-readable; extracted with `pdftotext`; used for ITT, compliance types, LATE, AIR assumptions, Wald ratio, and `ivreg()` inference warning.
- `Study Guides/mastering_metrics_ch5_dd_1pager.md` — used for DiD, common trends, state/year FE, and multistate panel framing.
- `Study Guides/exercises_gap_scan.md` — used for known pre-midterm gaps and professor-preferred exercise notation, especially Cov/Var OVB, bias recovery, ITT/take-up, and percentage-point conventions.
- `Course Admin/syllabus_extracted.md` and `Course Admin/QM3_Syllabus.pdf` — used to confirm midterm timing, course emphasis, and Week 3-6 topic ordering.
- Tyche memory files `GPEC 446 - QM3 - Valasquez/_agent/AGENT_CONTEXT.md` and `FEEDBACK.md` — used for course arc, professor tendencies, and ReportLab notation cautions.

New Canvas/inbox calibration files:

- `inbox/QM3/week3_IV_exercise_v2.pdf` — machine-readable; extracted with `pdftotext`; used to calibrate IV/LATE exercise style: anti-malarial two-sided noncompliance, ITT = 11% - 17% = -6 pp, first stage = 60% - 45% = 15 pp, LATE = -40 pp; Card-style schooling IV regression naming and reduced-form/first-stage ratio.
- `inbox/QM3/Interpreting all β's in DiD.pdf` — machine-readable; extracted with `pdftotext`; used to calibrate DiD coefficient interpretation: beta0 control-pre baseline, beta1 pre-treatment treated-control difference, beta2 control-group time trend, beta3 causal DiD effect.
- `inbox/QM3/Week 6 Exercises DiD FE FD.pdf` — machine-readable; extracted with `pdftotext`; used to calibrate DiD/first-difference/fixed-effect equivalence in the two-period business-training example.

## Sources Skipped

No OCR/scanned/handwritten source was needed. All PDFs used for this build produced meaningful machine-readable text with `pdftotext`.

I did not OCR or extract images from:

- `.pptx` exercise decks beyond what was already summarized in `exercises_gap_scan.md`
- any `.png`, `.docx`, or homework output files

Rationale: the task explicitly requested machine-readable PDF extraction only, and the new Canvas PDF files supplied enough text for calibration without OCR.

## Gaps / Caveats

- No official midterm practice exam was present in `Exam Materials/`; depth is calibrated from in-class exercises and syllabus topic order.
- Wooldridge Ch. 13/14 files were not present locally, so fixed-effects/DiD coverage relies on the syllabus, generated study guides, Mastering 'Metrics Ch. 5 one-pager, and Canvas exercises.
- Matching/synthetic control appears as Week 6 on the syllabus, but no new matching/synthetic-control Canvas files were provided in `inbox/QM3/`. The PDF treats matching only as a future/adjacent concept via existing lecture-reference notes, not as a full midterm page.
- The PDF is intentionally compact and exam-facing. It is a reference sheet, not a full replacement for the lecture/lab manuals.

## Verification

- `pdftotext` extraction succeeded for all source PDFs used.
- `python3 Study Guides/build_qm3_midterm_methods_reference.py` generated the PDF successfully.
- `pypdf` verification confirmed the generated PDF has 9 pages and 7 outline/bookmark entries.
- `pdftotext` on the generated PDF confirmed the expected title and method-page content are extractable.

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5.5 (medium reasoning)
Sources: QM3 generated reference manuals, QM3 syllabus extraction, Tyche memory, and machine-readable Canvas PDFs in `inbox/QM3/`
Agent: Tyche
---
