# GPEC 446 Homework 2

This folder contains the working files for **GPEC 446 — Quantitative Methods 3, Homework 2: Panel and Regression Discontinuity**.

The assignment has two parts:

- **Part I:** panel data, country fixed effects, two-way fixed effects, event-study timing, and population-weighted estimates for African governance and GDP.
- **Part II:** regression discontinuity around the Maimonides' Rule enrollment cutoff of 40 students, using the fifth-grade school dataset.

## What To Submit

The assignment prompt asks for both:

- a PDF with the numbered answers, tables, and figures
- the `.R` file or files used for the analysis

Current submission candidates:

- `Homework2EdgarAgunias.docx`
- `Homework_2_Integrated.R`

Before submitting, Edgar should read the integrated R script once and make sure he can explain the main blocks, especially the World Bank join, fixed-effects models, event-study construction, RD bandwidth choice, and `rdrobust` output.

## Main Files

- `Homework2EdgarAgunias.docx` — active Word working document.
- `Homework_2_Integrated.R` — current all-in-one script for Part I and Part II. This writes HTML tables, figures, notes, and `summary_output.txt` directly to this folder.
- `Homework_2_Part_I_panel.R` — older separate Part I script retained as a backup/reference.
- `Homework_2_Part_II_rdd.R` — older separate Part II script retained as a backup/reference.
- `PART_I_NOTES.md` — generated Part I notes and interpretation source.
- `PART_II_NOTES.md` — generated Part II notes and interpretation source.
- `build_homework_2_report.sh` — rebuilds the answer PDF from Markdown through HTML/headless Chrome.
- `report.css` — print styling for the generated HTML/PDF.

## Drafts Folder

`drafts/` holds generated or superseded answer drafts so the assignment root stays focused on active submission files, scripts, source data, and outputs:

- `drafts/Homework_2_Agunias_Draft.md` — Markdown source for the generated answer draft.
- `drafts/Homework_2_Agunias_Draft.html` — intermediate HTML used to build the generated PDF.
- `drafts/Homework_2_Agunias_Draft.pdf` — generated PDF answer draft.
- `drafts/Homework_2_Code_Thought_Process.md` — plain-English companion explaining the logic behind each question and the code structure.
- `drafts/Homework_2_Report_Skeleton.md` — earlier integration skeleton with Q1-Q9 headings.

## Source Data and Prompt Files

- `Homework_2_QM3-1.pdf` — clean assignment prompt with Q1-Q9 numbering.
- `Homework 2_ Panel & RDD.pdf` — Canvas wrapper/prompt export.
- `Africa_GDP.Rda` — governance panel for Part I.
- `grade5.dta` — fifth-grade school data for Part II.
- `rdd_paper.pdf` — assigned Angrist and Lavy (1999) paper. This local PDF is scan-only, so text extraction is limited.

## Current Base-Folder Outputs

The integrated script writes Word-copy-friendly tables and figures directly to the Homework 2 folder:

- Part I tables: `table_q1_pooled_within.html`, `table_q2_twfe_bigimp.html`, `table_q4_representative_person.html`
- Part I event-study outputs: `event_study_leadlag_coefficients.html`, `event_study_residual_means.html`, `weighted_event_study_residual_means.html`, and related `figure_q*.png` files
- Part II tables: `grade5_schema.html`, `manual_local_linear_results.html`, `rdrobust_default_results.html`
- Part II figures: `hist_school_enrollment.png`, `rdd_classize_cutoff40.png`, `rdd_avgmath_cutoff40.png`, `rdd_avgverb_cutoff40.png`
- Notes and summary: `PART_I_NOTES.md`, `PART_II_NOTES.md`, `summary_output.txt`

## Older Output Folders

`outputs/part_i/` contains the generated Part I panel files:

- cleaned analysis panel
- missing World Bank join audit
- Q1/Q2/Q4 CSV tables
- event-study CSV summaries
- event-study figures

`outputs/part_ii/` contains the generated Part II RDD files:

- data schema audit
- enrollment histogram
- class-size and score RD plots
- manual local-linear RD results
- `rdrobust` default results
- terminal summary output

`outputs/part_ii/R_libs/` is a local package library created during analysis. It is not a submission artifact and should not be staged unless explicitly needed.

## How To Rebuild The Analysis

From this folder:

```bash
Rscript --vanilla Homework_2_Integrated.R
./build_homework_2_report.sh
```

The integrated script fetches World Bank GDP per capita and population data, so it needs internet access. It also uses `outputs/part_ii/R_libs` only to load the locally installed `rdrobust` package. The build script reads and writes the generated answer draft in `drafts/`.

## Macro Workflow

1. Part I loads the Africa governance panel and keeps 1985-1998.
2. It joins World Bank GDP per capita and population data to the governance panel.
3. It estimates pooled OLS, country/year fixed effects, TWFE around `bigimp`, and a Lab 5-style event-study coefficient figure with year -1 as the omitted reference period.
4. It repeats the core relationship using population weights to shift from average country-year to representative person-year.
5. Part II loads `grade5.dta`, creates the running variable around the cutoff of 40, and checks the enrollment distribution.
6. It plots class size, math scores, and verbal scores around the cutoff.
7. It estimates manual local-linear RD effects and then compares them to `rdrobust`.
8. It runs a falsification/smoothness test using `disadvantaged`.
9. The report pulls those outputs into a numbered Q1-Q9 answer draft.

## Known Caveats

- Part I leaves 21 country-year rows unmatched or missing after the World Bank join, concentrated in Eritrea and Somalia.
- The local Angrist and Lavy PDF is scan-only, so the Q5 explanation relies on assignment context plus citation metadata rather than direct text extraction from the PDF.
- The RD estimates are suggestive but imprecise; the `rdrobust` confidence intervals include zero.
- The PDF draft is a strong working candidate, but Edgar should review for voice and code explainability before submission.

---
Generated for: Edgar Agunias
Date: 2026-05-19
Model: GPT-5 Codex
Sources: Homework 2 assignment files, generated Part I and Part II scripts/outputs, Homework 2 thought-process companion
Agent: Tyche
---
