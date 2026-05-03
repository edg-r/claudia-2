# GPPS 463 Midterm Theory Reference v1.2.0 -- Source Notes

## Purpose

This notes file documents the v1.2.0 revision of `GPPS_463_Midterm_Theory_Reference_v1.2.0.pdf`. The revision builds directly on the v1.1.0 PDF and `build_midterm_theory_reference.py`.

## Revision Scope

- Increased the builder's body text style to 12pt, per Edgar's request.
- Expanded each theory/framework entry with:
  - author or lecture-context setup;
  - fuller mechanism framing;
  - course-vocabulary and assumptions presented in a compact paired table;
  - explicit exam-application guidance;
  - case/comparison cues for applied essay use.
- Tightened page margins and section spacing to preserve readability with the larger body text.
- Preserved the 11-framework scope and continued to skip History of Warfare.
- Preserved model provenance as `GPT-5.5 (medium reasoning)`.

## Layout Note

With 12pt body text and fuller theory treatment, the old one-page-per-framework layout no longer fits without cutting substance or reducing below 12pt. v1.2.0 therefore uses a fuller two-page spread per framework: one cover/TOC page plus 11 framework spreads, 23 pages total. Sidebar bookmarks and TOC links land on the first page of each framework.

## Sources Used

The v1.2.0 revision reused the v1.1.0 source base:

- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/Midterm_1_Study_Guide.md`
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/Midterm_1_Index_Cards.md`
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/Midterm_1_Lecture_Gaps.md`
- `GPPS 463 - Pol SEA - Ravanilla/W2 - Sinivs Indi, Guns Germs & Steel/Week 2 Reference Summary.pdf`
- `GPPS 463 - Pol SEA - Ravanilla/W3 - Colonial Institutions and Development/W3 Theory Reference.pdf`
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Week_4_Reference.pdf`
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/jansen2001_thailand_miracle_summary.md`
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/huff1995_singapore_model_summary.md`
- `GPPS 463 - Pol SEA - Ravanilla/W5 - Singapore & Asian Financial Crisis/Discussion Post LD10 - Asian Financial Crisis.md`
- `GPPS 463 - Pol SEA - Ravanilla/Course Admin/syllabus_extracted.md`
- `GPPS 463 - Pol SEA - Ravanilla/_agent/AGENT_CONTEXT.md` and `FEEDBACK.md`

## Build / Verification

- Builder: `GPPS 463 - Pol SEA - Ravanilla/Study Guides/build_midterm_theory_reference.py`
- Output: `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.2.0.pdf`
- Tooling: ReportLab and pypdf.
- Verification performed:
  - Generated the PDF successfully.
  - Confirmed page count is 23: one cover page plus 11 two-page theory/framework spreads.
  - Confirmed PDF outline/bookmarks are present for all 11 framework pages.
  - Confirmed bookmark destinations map to pages 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, and 22.
  - Confirmed 11 clickable TOC link annotations on the cover page and no malformed link annotations.
  - Confirmed no blank pages.
  - Confirmed text extraction returns 45,979 characters.
  - Confirmed extracted PDF text contains `GPT-5.5 (medium reasoning)`.
  - Confirmed extracted PDF text contains `AUTHOR / TIME-PERIOD CONTEXT`, `EXAM APPLICATION`, and `CASE / COMPARISON CUES`.
  - Confirmed the builder defines `styles["Body"]` with `fontSize=12`.

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
