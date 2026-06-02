# GPCO 410 Midterm Theory Reference v1.1.0 — Source Notes

## Deliverable

- PDF: `GPCO410_Midterm_Theory_Reference_v1.1.0.pdf`
- Builder: `build_midterm_theory_reference.py`
- Supersedes: `GPCO410_Midterm_Theory_Reference_v1.0.0.pdf`
- Scope: midterm prep for GPCO 410, covering the syllabus window before the May 4, 2026 in-class midterm: W1-W5.

## Revision From v1.0.0

- Expanded each one-page theory entry so the theory section fills the page more fully while preserving the same exam-ready structure: situation, core intuition, key concepts, assumptions, strengths, and weaknesses.
- Revised the header source line for each theory so it names the full article, paper, or book chapter title first, followed by the author(s).
- Preserved source-faithful terminology, especially Powell's commitment-problem language and Cederman, Hug, and Krebs's governmental-conflict / conflict-over-government / territorial-conflict distinction.
- Updated provenance in the builder and notes from generic model references to `GPT-5.5 (medium reasoning)`.
- Preserved the v1.0.0 PDF and notes as prior-version artifacts while generating v1.1.0 outputs.

## Sources Used

- `Course Admin/syllabus_extracted.md` for exam date, W1-W5 ordering, and reading/session map.
- `_agent/THEORIES.md` for cumulative W1-W3 theory continuity.
- `_agent/AGENT_CONTEXT.md` and `_agent/FEEDBACK.md` for Praether/Ali expectations and source-faithful terminology rules.
- `Study Guides/pre_midterm_strategy.md` for midterm timing, Orange-memo context, and OCR tractability notes.
- `Study Guides/Sec/GPCO410_W3_TheoryReference.pdf` for Fearon, Powell, Morrow, Saddam/Yetiv, and Ukraine negotiation framing.
- `Study Guides/GPCO_410_Week_4_Reference.pdf` for W4 democratic peace and civil-war structure.
- `Study Guides/fearon_audience_costs_theoryref.md` and `.pdf` for Fearon 1994 audience costs.
- `Study Guides/buenodemesquita_etal_institutional_dp_theoryref.md` and `.pdf` for selectorate/institutional democratic peace.
- `Study Guides/GPCO410_W4_Herrmann_Tetlock_Visser_theory_ref.pdf` for cognitive-interactionist public-opinion theory.
- `Study Guides/walter_committing_to_peace_ch2_theoryref.md` and `.pdf` plus `class9_walter_committing_to_peace_ch2_1page_summary.md` for Walter's negotiated-settlement commitment problem.
- `Study Guides/blattman_miguel_2010_civil_war_summary.md` and `walter_2009_bargaining_failures_civil_war_summary.md` for the civil-war onset/correlates page.
- `Assignments/Orange Memo - Myanmar/reading_notes.md` and Athena memory entries for Cederman, Hug, and Krebs terminology.
- Original W1/W2 source PDFs were checked for source-title fidelity, including Lake and Powell, Muthoo, Frieden, Schelling, Milner, Lebow, Russell, and the signaling notes.

## OCR / Scan Rationale

Skipped OCR. Machine-readable sources were sufficient:

- `pdftotext` is available locally.
- `pypdf`, `pdfplumber`, and `reportlab` are installed.
- Prior Week 3 and Week 4 theory PDFs yielded extractable text.
- Walter Chapter 2 has an existing Athena theory reference and one-page summary based on the course reading. The local pre-midterm strategy noted the original assigned PDF was image-only, but the existing generated material already captures the theory at the level needed for the reference document.

OCR should only be revisited if Edgar wants direct quotations/page-number verification from the scanned Walter Chapter 2 PDF.

## Verification

- Generated `GPCO410_Midterm_Theory_Reference_v1.1.0.pdf` with ReportLab from `build_midterm_theory_reference.py`.
- Verified PDF page count: 12 pages, equal to 1 cover page plus 11 theory pages.
- Verified PDF sidebar bookmarks: 11 entries, one for each theory page.
- Verified cover-page internal links: 11 link annotations on page 1.
- Verified text extraction with `pypdf`: all pages extract text, full source-title header lines appear, and `GPT-5.5 (medium reasoning)` appears in the generated PDF.
- Verified no remaining generic model-provenance strings in the Study Guides folder text files after the notes/provenance correction. The preserved v1.0.0 PDF still contains its historical embedded text.

## References

Blattman, C., & Miguel, E. (2010). Civil war. *Journal of Economic Literature*, *48*(1), 3-57. https://doi.org/10.1257/jel.48.1.3

Bueno de Mesquita, B., Morrow, J. D., Siverson, R. M., & Smith, A. (1999). An institutional explanation of the democratic peace. *American Political Science Review*, *93*(4), 791-807.

Cederman, L.-E., Hug, S., & Krebs, L. F. (2010). Democratization and civil war: Empirical evidence. *Journal of Peace Research*, *47*(4), 377-394.

Fearon, J. D. (1994). Domestic political audiences and the escalation of international disputes. *American Political Science Review*, *88*(3), 577-592.

Fearon, J. D. (1995). Rationalist explanations for war. *International Organization*, *49*(3), 379-414.

Herrmann, R. K., Tetlock, P. E., & Visser, P. S. (1999). Mass public decisions to go to war: A cognitive-interactionist framework. *American Political Science Review*, *93*(3), 553-573.

Powell, R. (2006). War as a commitment problem. *International Organization*, *60*(1), 169-203.

Walter, B. F. (2002). *Committing to peace: The successful settlement of civil wars*. Princeton University Press.

Walter, B. F. (2009). Bargaining failures and civil war. *Annual Review of Political Science*, *12*, 243-261.

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5.5 (medium reasoning)
Sources: GPCO 410 syllabus extraction, Athena theory tracker and memory, prior W3/W4/W5 generated theory references, W1/W2 source PDFs for title fidelity, Walter/Fearon/Bueno de Mesquita/Herrmann guides, Orange Memo source notes
Agent: Athena
---
