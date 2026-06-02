# Tyche — GPEC 446 Feedback Log

Corrections and confirmed good approaches. Read this before every session.

<!-- No entries yet. Append new feedback below this line. -->

### 2026-04-30 — QM3 lecture reference sheet readability patch
**Type:** correction
**What:** Edgar flagged that formula/notation text in v1.2.0 ran off the page, CIA was not clearly explained on first use, and numbered lecture-reference topics needed short "Explain Like I'm 5" conclusions.
**Why:** Study guides need to be visually reliable as PDFs and should decode acronyms and formulas without forcing Edgar to infer missing context.
**Rule going forward:** For QM3 reference PDFs, verify formula/code block bounds after rendering, expand acronyms as Full Name (ABBREVIATION) on first use, and include a compact plain-English takeaway for each major numbered topic.

### 2026-05-24 — R homework scripts should stay analysis-only
**Type:** correction
**What:** Edgar clarified that `Homework_2_Integrated.R` should not include embedded prose/note-writing sections such as `summary_output.txt`, `part_i_notes`, `part_ii_notes`, `writeLines()` narrative notes, or `cat()`/`sink()` summary prose.
**Why:** Interpretation belongs in the homework document, while the R script should stay clean, simple, and focused on reproducible analysis outputs/tables/figures.
**Rule going forward:** For QM3 homework scripts, avoid embedded prose or note-writing sections unless Edgar explicitly requests them; keep interpretation in the document and keep scripts focused on data prep, models, tables, and figures.
