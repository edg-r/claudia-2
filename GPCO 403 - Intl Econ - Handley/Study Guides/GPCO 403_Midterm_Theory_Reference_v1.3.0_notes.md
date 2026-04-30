# GPCO 403 Midterm Theory Reference v1.3.0 Notes

## Deliverable

- PDF: `GPCO 403_Midterm_Theory_Reference_v1.3.0.pdf`
- Matching notes: `GPCO 403_Midterm_Theory_Reference_v1.3.0_notes.md`
- Build script: `build_midterm_theory_reference.py`
- Date built: 2026-04-29
- Agent: Plutus

## Revision Summary

Version 1.3.0 starts from the v1.2.0 theory set and source base, but rebuilds the layout for Edgar's larger-text request. The body text is drawn at 12pt in the builder, the theory pages use landscape orientation with tighter margins, and each theory still occupies exactly one page. History of Warfare material remains skipped.

Changes from v1.2.0:

1. Changed output target from `v1.2.0` to `v1.3.0`; v1.2.0 was not overwritten.
2. Rebuilt each theory page around 12pt body text instead of the prior compact ~6pt ReportLab paragraph styles.
3. Added an `AUTHOR / SOURCE CONTEXT` block to every theory page so Edgar sees the author/source environment before the mechanism.
4. Expanded the main theory explanation into a larger `SITUATION + MECHANISM` block with exam logic.
5. Preserved one page per theory by using landscape pages, tighter margins, and compact supporting boxes for key terms, assumptions, strengths, weaknesses, and exam applications.
6. Added an overflow detector to the builder: if a text box clips lines, the script reports the affected box and exits with failure.
7. Kept model provenance as `GPT-5.5 (medium reasoning)`.

## Theory Pages Included

1. National income accounting and open-economy GDP
2. Current account and balance of payments identity
3. Savings-investment gap and twin deficits
4. External wealth and valuation effects
5. Intertemporal trade and consumption smoothing
6. Exchange-rate basics and cross-rate arbitrage
7. Interest parity and forward exchange rates
8. Exchange-rate regimes and crisis balance sheets
9. Law of one price
10. Purchasing power parity and the real exchange rate
11. Big Mac Index as applied PPP

## Primary Sources Used

- `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.2.0.pdf`
- `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.2.0_notes.md`
- `GPCO 403 - Intl Econ - Handley/Study Guides/2026-04-27_ppp_loop_big_mac_1pager.md`
- `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Week_4_Reference.pdf`
- `GPCO 403 - Intl Econ - Handley/W5 - Midterm Review/gpco403_spring2021_midterm_shortanswer_solutions_withoutQ3.pdf`
- `inbox/Intl Econ/International_Econ_Midterm2025_answerkey.pdf`
- `GPCO 403 - Intl Econ - Handley/W5 - Midterm Review/Practice_questions.pdf`
- `inbox/Intl Econ/GPCO403_Lecture6_20apr2026.pptx`
- `inbox/Intl Econ/GPCO403_Lecture7_PPP_22apr2026.pptx`
- `GPCO 403 - Intl Econ - Handley/W5 - Midterm Review/Equations_Midterm_1.pdf`

## Verification

- Rebuilt with `python3 GPCO\ 403\ -\ Intl\ Econ\ -\ Handley/Study\ Guides/build_midterm_theory_reference.py`.
- Builder overflow detector completed cleanly after layout tuning.
- Verified with `pypdf`: 13 pages total.
- Verified structure: 1 cover/TOC page + 11 theory pages + 1 references/disclosure page.
- Verified PDF sidebar bookmarks: 11 outline entries, one for each theory.
- Verified TOC/link annotations: 11 annotations.
- Verified text extraction:
  - `AUTHOR / SOURCE CONTEXT` appears 11 times.
  - All theory-page section labels appear 11 times.
  - `GPT-5.5 (medium reasoning)` appears in the PDF provenance.
  - Older generic model-provenance strings do not appear.
- Verified builder body drawing uses `size = 12`.

## Caveats

- The 12pt constraint means supporting lists are more selective than v1.2.0. The fuller explanation is concentrated in the source-context and mechanism blocks.
- The PDF uses landscape pages to preserve one page per theory while keeping text readable.

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5.5 (medium reasoning)
Sources: v1.2.0 theory reference and notes; Spring 2021 and 2025 midterm answer keys; practice questions; Lecture 6 and Lecture 7 PPP slides; Equations_Midterm_1 formula check
Agent: Plutus
---
