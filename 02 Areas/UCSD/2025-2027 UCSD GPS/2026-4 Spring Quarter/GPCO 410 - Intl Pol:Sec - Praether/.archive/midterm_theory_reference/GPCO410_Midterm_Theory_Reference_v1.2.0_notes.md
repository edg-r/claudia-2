# GPCO 410 Midterm Theory Reference v1.2.0 — Source Notes

## Deliverable

- PDF: `GPCO410_Midterm_Theory_Reference_v1.2.0.pdf`
- Builder: `build_midterm_theory_reference.py`
- Supersedes: `GPCO410_Midterm_Theory_Reference_v1.1.0.pdf`
- Scope: midterm prep for GPCO 410, covering the syllabus window before the May 4, 2026 in-class midterm: W1-W5.

## Revision From v1.1.0

- Increased the builder's main `Body` paragraph style to 12pt font.
- Expanded every theory entry with new `AUTHOR / READING CONTEXT`, `MECHANISM`, `EXAM DEPLOYMENT LOGIC`, `COMMON PITFALL`, and `COMPARE WITH` material.
- Preserved the same 11-theory syllabus sequence and clickable cover/sidebar navigation.
- Allowed expanded theory entries to breathe across two pages rather than forcing compressed one-page entries with tiny text.
- Preserved source-faithful terminology, especially:
  - Powell: commitment problems as the master mechanism, with preventive war / power-shifting bargains / first-strike dynamics treated as illustrations rather than a separate taxonomy.
  - Cederman, Hug, and Krebs: democratization, governmental conflict, conflict over government, and territorial conflict.
  - Fearon: private information, incentives to misrepresent, commitment problems, and issue indivisibility as rationalist mechanisms.
  - Walter: implementation, demobilization vulnerability, third-party security guarantees, and power sharing.
- Kept provenance as `GPT-5.5 (medium reasoning)`.
- History of Warfare material remains intentionally skipped.

## Sources Used

- `Course Admin/syllabus_extracted.md` for exam date, W1-W5 ordering, and reading/session map.
- `_agent/THEORIES.md` for cumulative W1-W3 theory continuity.
- `_agent/AGENT_CONTEXT.md` and `_agent/FEEDBACK.md` for Praether/Ali expectations, source-faithful terminology rules, and Cederman/Powell wording constraints.
- `Study Guides/GPCO410_Midterm_Theory_Reference_v1.1.0.pdf` and `build_midterm_theory_reference.py` as the base artifact and builder.
- `Study Guides/GPCO410_Midterm_Theory_Reference_v1.1.0_notes.md` for prior source trail and verification baseline.
- `Study Guides/pre_midterm_strategy.md` for midterm timing, Orange-memo context, and OCR tractability notes.
- `Study Guides/Sec/GPCO410_W3_TheoryReference.pdf` for Fearon, Powell, Morrow, Saddam/Yetiv, and Ukraine negotiation framing.
- `Study Guides/GPCO_410_Week_4_Reference.pdf` for W4 democratic peace and civil-war structure.
- `Study Guides/fearon_audience_costs_theoryref.md` and `.pdf` for Fearon 1994 audience costs.
- `Study Guides/buenodemesquita_etal_institutional_dp_theoryref.md` and `.pdf` for selectorate/institutional democratic peace.
- `Study Guides/GPCO410_W4_Herrmann_Tetlock_Visser_theory_ref.pdf` for cognitive-interactionist public-opinion theory.
- `Study Guides/walter_committing_to_peace_ch2_theoryref.md` and `.pdf` plus `class9_walter_committing_to_peace_ch2_1page_summary.md` for Walter's negotiated-settlement commitment problem.
- `Study Guides/blattman_miguel_2010_civil_war_summary.md` and `walter_2009_bargaining_failures_civil_war_summary.md` for the civil-war onset/correlates page.
- `Assignments/Orange Memo - Myanmar/reading_notes.md` and Athena memory entries for Cederman, Hug, and Krebs terminology.

## OCR / Scan Rationale

Skipped OCR. Machine-readable sources and existing Athena-generated study guides were sufficient for the revision.

- `pdftotext` is available locally.
- `pypdf`, `pdfplumber`, and `reportlab` are installed.
- Prior Week 3 and Week 4 theory PDFs yielded extractable text.
- Walter Chapter 2 has an existing Athena theory reference and one-page summary based on the course reading.

OCR should only be revisited if Edgar wants direct quotations/page-number verification from the scanned Walter Chapter 2 PDF.

## Verification

- Generated `GPCO410_Midterm_Theory_Reference_v1.2.0.pdf` with ReportLab from `build_midterm_theory_reference.py`.
- Verified PDF page count: 23 pages, equal to 1 cover page plus 22 expanded theory-content pages.
- Verified PDF sidebar bookmarks: 11 entries, one for each theory.
- Verified cover-page internal links: 11 link annotations on page 1.
- Verified text extraction with `pypdf`: all 23 pages extract text.
- Verified expanded section labels extract from the PDF: `AUTHOR / READING CONTEXT`, `MECHANISM`, `EXAM DEPLOYMENT LOGIC`, `COMMON PITFALL`, and `COMPARE WITH`.
- Verified source-faithful terminology extracts from the PDF, including `governmental conflict`, `territorial conflict`, and `commitment problems are the master mechanism`.
- Verified provenance extracts from the PDF as `GPT-5.5 (medium reasoning)`.
- Verified builder body style: `styles.add(ParagraphStyle(name="Body", ... fontSize=12 ...))`.

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
Sources: GPCO 410 syllabus extraction, Athena theory tracker and memory, prior v1.1.0 midterm theory reference, prior W3/W4/W5 generated theory references, Walter/Fearon/Bueno de Mesquita/Herrmann guides, Orange Memo source notes
Agent: Athena
---
