# Tyche — GPEC 446 Agent Context

## Course Info
- **Course:** GPEC 446 — Quantitative Methods 3
- **Professor:** Valasquez
- **Term:** Spring 2026
- **Textbook:** Angrist & Pischke, *Mastering 'Metrics*

## Course Arc
Lecture sequence as of 2026-04-15 (materials received for L1-L5, Labs 1-2). **Note: folder-week-number and syllabus-week-number are NOT the same.** The course folders are labelled by lecture order; the syllabus uses week-of-instruction. When in doubt, the syllabus governs.

| Lecture | Folder | Syllabus Week | Topic |
|---|---|---|---|
| L1 Intro | `W1 - Intro & Randomisation/` | Week 1 | Course setup, randomisation (Lab 1) |
| L2 Causal Inference | `W2 - Causal Inference/` | Week 2 | Potential outcomes (Lab 2 intro_causal_inference) |
| L3 Regression | `W3 - Regression/` | Week 2 | OLS fundamentals |
| L4 Regression 2 | `W3 - Regression/` | Week 3 | Multivariate / controls |
| L5 Instrumental Variables | `W4 - Instrumental Variables/` | **Week 3** | IV estimation (*Mastering 'Metrics* Ch. 3) |
| (not yet posted) | — | **Week 4** | Panel Data Basics: FE, DiD, parallel trends (*Mastering 'Metrics* Ch. 5) |

Syllabus Week 4 is **Panel Data Basics (FE + DiD)**, NOT IV. The course folder `W4 - Instrumental Variables/` contains what the syllabus calls Week 3 material. Week 4 panel-data slides have not been posted as of 2026-04-16. Any "Week 4" reference by Valasquez or the TA should be read as panel data.

Course folder is organized week-by-week (W1, W2, ...) by lecture sequence, mirroring Edgar's GPCO 410 and GPPS 463 layouts. Syllabus lives in `Course Admin/`. Textbook (Angrist & Pischke, *Mastering 'Metrics*) is at course root.

## Professor Tendencies
- Uses Cov/Var notation for OVB in exercises: c1 = Cov(Y,W)/Var(W), c2 = Cov(W,X)/Var(X), Bias = c1×c2. Equivalent to π1×γ but the exercise handouts prefer the Cov/Var form. Study-guide material should present both notations side by side.
- In-class exercises use concrete program contexts (Bono Familias CCT, police/crime, welfare/poverty, schooling/earnings) rather than abstract variable names. Expect exercise prompts to set up the policy scenario in prose before asking the technical question.
- Tests ITT/take-up vocabulary in Week 1 even though the syllabus defers ITT/LATE to Week 9. Week 1 Exercise 3d: "Only 65% of eligible households took up the program... what effect does the 11 pp estimate capture, and what additional assumption would you need to recover the effect on takers?" Expect students to know ITT by name and the ITT ≠ ATT distinction from day one.
- Includes an AI-prompting meta-exercise (Week 1 Exercise 5) contrasting naive and optimal prompts. Emphasises that precise numerical context ("percentage points", specific values, program name) prevents AI hallucination.
- Professor name normalisation: "Mateo Vasquez-Cortes" in the lab handouts, "Vásquez-Cortés" in the lecture reference manuals, "Valasquez" in the course folder naming. Lab lead is David L. Vargas.

## Edgar's Study Method — Confirm-Then-Sharpen
Edgar's conceptual-tutoring pattern is to state his current intuition in plain language and ask the agent to confirm or sharpen rather than explain from scratch. The workflow that works: (1) affirm what's right in his framing, (2) add one precision point or edge case he hasn't surfaced yet, (3) anchor the abstraction in a concrete running example — the PACES voucher lottery for IV/LATE, the Dale-Krueger elite-college matching setup for CIA/common support, the manual's IQ/earnings reparameterization for demeaning. Confirm-then-sharpen beats correct-from-scratch for his learning style; do not restart from first principles when his intuition is already 80% there. Validated across an 8-turn IV tutoring thread on 2026-04-16 covering ITT, LATE, Wald, four AIR assumptions, weak first stage (Bound/Jaeger/Baker, Staiger-Stock F>10 vs Lee et al. F>104.7), weak-IV-robust inference, demeaning, and CIA + common support.

## Cross-Course Links
- Quantitative methods apply across all courses, especially data analysis in GPCO 403 (Plutus)
- Causal inference frameworks relevant to political science readings in GPCO 410 (Athena) and GPPS 463 (Poseidon)

## Reading-Summary Default (effective 2026-04-22)
Edgar's new default for reading summaries is `_claudia/skills/theory-reference-pdf.md`, not BLUF/memo-summarizer. BLUF (`memo-summarizer.md`) is retained only for policy-memo intake and synthesis briefs. When Edgar requests a chapter/article summary without specifying format, default to the theory-reference-pdf skill.

## Build Conventions — ReportLab glyph handling
QM3 notation uses Y̅ (Y with combining macron), τ̂ (tau-hat), X̂ (X-hat), and similar. Helvetica and Courier built-in ReportLab fonts DO NOT include combining macron (U+0304) or precomposed Ȳ (U+0232) — they render as black boxes. Fix: register Arial Unicode via `pdfmetrics.registerFont(TTFont('ArialUnicode', '/Library/Fonts/Arial Unicode.ttf'))` and wrap every problematic glyph in `<font face="ArialUnicode">...</font>` inside Paragraph XML. The `<sup>^</sup>` pattern works fine with all Greek letters in Helvetica/Courier (no font-face override needed for β̂, τ̂, π̂, γ̂), so only the combining-diacritic cases need the Arial Unicode wrap. See v2 build of `QM3_Lectures_Reference_Manual.pdf` (2026-04-16) for the reference implementation.
