# GPPS 463 Midterm Theory Reference v1.0.0 — Source Notes

## Purpose

This notes file documents the source handling for `GPPS_463_Midterm_Theory_Reference_v1.0.0.pdf`. The PDF is a structured exam reference built with `_claudia/skills/theory-reference-pdf.md` and `_claudia/skills/pdf.md`: one page per framework, consistent situation/core intuition/concepts/assumptions/strengths/weaknesses structure, clickable TOC, and PDF sidebar bookmarks.

## Sources Used

- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/Midterm_1_Study_Guide.md`
  - Used as the main baseline for W1-W3 reading coverage, SAQ calibration, and named concepts.
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/Midterm_1_Index_Cards.md`
  - Used to compress each Midterm 1 reading into exam-ready concepts and case hooks.
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/Midterm_1_Lecture_Gaps.md`
  - Used for lecture-only frameworks: constructed region, five constraints to institutions, European Diversion, Inclusive/Extractive 2x2, Dutch optimization menu, Philippines chain, and Anderson/North reminders.
- `GPPS 463 - Pol SEA - Ravanilla/W2 - Sinivs Indi, Guns Germs & Steel/Week 2 Reference Summary.pdf`
  - Machine-readable text extracted with `pypdf`; used to verify Dell, Lane, and Querubin framing.
- `GPPS 463 - Pol SEA - Ravanilla/W3 - Colonial Institutions and Development/W3 Theory Reference.pdf`
  - Machine-readable text extracted with `pypdf`; used to preserve the existing W3 theory-reference structure and terminology.
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Week_4_Reference.pdf`
  - Machine-readable text extracted with `pypdf`; used to extend the theory reference to Jansen and the Asian Miracle.
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/jansen2001_thailand_miracle_summary.md`
  - Used for Jansen's Thailand mechanism and limits.
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/huff1995_singapore_model_summary.md`
  - Used for the Singapore model page.
- `GPPS 463 - Pol SEA - Ravanilla/W5 - Singapore & Asian Financial Crisis/Discussion Post LD10 - Asian Financial Crisis.md`
  - Used only for the already-approved Hicken discussion-post framing: the crisis-severity paradox and 2008 timing test.
- `GPPS 463 - Pol SEA - Ravanilla/Course Admin/syllabus_extracted.md`
  - Used for course sequence, lecture-day mapping, and reading scope.
- `GPPS 463 - Pol SEA - Ravanilla/_agent/AGENT_CONTEXT.md`, `FEEDBACK.md`, and `TASK_LOG.md`
  - Used for Poseidon course style and prior-task continuity.

## Sources Checked But Not Used

- `inbox/Intl Econ/*`
  - Skipped as GPCO 403 material, not GPPS 463.
- `inbox/QM3/*`
  - Skipped as GPEC 446 material, not GPPS 463.
- `inbox/bbi_autonomous_agent_prompt.md`
  - Skipped as unrelated to GPPS 463.
- `inbox/myanmar_democratization_outline.md`
  - Skipped because current course-memory notes indicate Myanmar memo work belongs to GPCO 410/Athena unless explicitly tied to GPPS 463.
- Post-LD10 GPPS 463 files for W6-W10
  - Skipped for v1.0.0 except where existing Poseidon memory already supplied LD11 context. This document is a midterm/theory reference, so it prioritizes material already summarized or already represented in study-guide form.

## OCR / Scan Handling

No OCR was run. The required source handling for this pass was machine-readable only. Existing PDFs used for verification had extractable text through `pypdf`, including the Week 2 reference summary, W3 theory reference, and Week 4 reference PDF. Files with `.preOCR.pdf` siblings were not reprocessed because their already-summarized outputs were sufficient and the task explicitly said not to redo summarized material from scratch.

## Gaps And Caveats

- The Hicken page is based on the existing LD10 discussion-post framing and Poseidon memory, not a fresh extraction of `hicken2008.pdf`.
- The Singapore page is based on the existing Huff summary, not a fresh extraction of `huff1995.pdf`.
- Week 4 optional readings listed in the Canvas schedule were not available in the workspace and were not summarized.
- This PDF is a study aid, not a substitute for the assigned readings or Ravanilla's lecture slides.

## Build / Verification

- Builder: `GPPS 463 - Pol SEA - Ravanilla/Study Guides/build_midterm_theory_reference.py`
- Output: `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.0.0.pdf`
- Tooling: ReportLab 4.4.5 and pypdf.
- Verification performed:
  - Generated the PDF successfully.
  - Confirmed page count is 12: one cover page plus 11 theory/framework pages.
  - Confirmed PDF outline/bookmarks are present for all 11 framework pages.
  - Confirmed the cover page remained page 1 and the first theory begins on page 2.

## References

Acemoglu, D., & Robinson, J. A. (2012). Reversing development. In *Why nations fail: The origins of power, prosperity, and poverty*. Crown.

Dell, M., Lane, N., & Querubin, P. (2018). The historical state, local collective action, and economic development in Vietnam. *Econometrica*, *86*(6), 2083-2121. https://doi.org/10.3982/ECTA15122

Dell, M., & Olken, B. A. (2020). The development effects of the extractive colonial economy: The Dutch Cultivation System in Java. *Review of Economic Studies*, *87*(1), 164-203. https://doi.org/10.1093/restud/rdz017

Diamond, J. (1997). Prologue: Yali's question. In *Guns, germs, and steel: The fates of human societies*. W. W. Norton.

Hayton, B. (2014). Wrecks and wrongs: Prehistory to 1500. In *The South China Sea: The struggle for power in Asia*. Yale University Press.

Hicken, A. (2008). The political economy of the Asian financial crisis. Course reading PDF.

Huff, W. G. (1995). What is the Singapore model of economic development? *Cambridge Journal of Economics*, *19*(6), 735-759.

Jansen, K. (2001). Thailand: The making of a miracle? *Development and Change*, *32*(3), 343-370.

Stubbs, R. (1999). War and economic development: Export-oriented industrialization in East and Southeast Asia. *Comparative Politics*, *31*(3), 337-355. https://www.jstor.org/stable/422343

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5.5 (medium reasoning)
Sources: Existing GPPS 463 study guides, Week 2/W3/W4 reference PDFs, syllabus extraction, Poseidon course memory
Agent: Poseidon
---
