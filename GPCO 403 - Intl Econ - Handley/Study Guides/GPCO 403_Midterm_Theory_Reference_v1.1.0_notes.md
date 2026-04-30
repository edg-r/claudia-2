# GPCO 403 Midterm Theory Reference v1.1.0 Notes

## Deliverable

- PDF: `GPCO 403_Midterm_Theory_Reference_v1.1.0.pdf`
- Matching notes: `GPCO 403_Midterm_Theory_Reference_v1.1.0_notes.md`
- Build script: `build_midterm_theory_reference.py`
- Date built: 2026-04-29
- Agent: Plutus

## Revision Summary

This version preserves the v1.0.0 structure and source base, but responds to Edgar's feedback that the theory treatment was too sparse. The document still uses the `theory-reference-pdf` structure: one cover/TOC page, one page per theory/framework, and one references/disclosure page.

Changes from v1.0.0:

1. Expanded every theory page inside the existing six-section template: situation, core intuition, key concepts, assumptions, strengths, and weaknesses.
2. Added fuller source/header lines for every theory page. Each header now names the relevant source or reading first, then the author(s).
3. Updated all model provenance from generic `ChatGPT-5`, `GPT-5`, or `GPT-5 via Codex` language to `GPT-5.5 (medium reasoning)`.
4. Kept version history intact by generating v1.1.0 outputs rather than overwriting v1.0.0.
5. Switched body bullet markers from the ReportLab bullet glyph to ASCII hyphens so PDF text extraction is cleaner.

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

- `GPCO 403 - Intl Econ - Handley/Course Admin/syllabus_extracted.md`
- `GPCO 403 - Intl Econ - Handley/_agent/AGENT_CONTEXT.md`
- `GPCO 403 - Intl Econ - Handley/_agent/READINGS.md`
- `GPCO 403 - Intl Econ - Handley/Study Guides/2026-04-27_ppp_loop_big_mac_1pager.md`
- `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Week_4_Reference.pdf`
- `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.0.0.pdf`
- `GPCO 403 - Intl Econ - Handley/Study Guides/GPCO 403_Midterm_Theory_Reference_v1.0.0_notes.md`
- `GPCO 403 - Intl Econ - Handley/W1 - Introduction & National Income/GPCO403_Lecture1.pptx`
- `GPCO 403 - Intl Econ - Handley/W1 - Introduction & National Income/GPCO403_Lecture2.pptx`
- `GPCO 403 - Intl Econ - Handley/W2 - Balance of Payments & Global Imbalances/GPCO403_Lecture3.pptx`
- `GPCO 403 - Intl Econ - Handley/W3 - External Wealth & Exchange Rates/GPCO403_Lecture5.pdf`
- `GPCO 403 - Intl Econ - Handley/W3 - External Wealth & Exchange Rates/GPCO403_Lecture7.pdf`
- `GPCO 403 - Intl Econ - Handley/W4 - PPP, LOOP & Big Mac Application/GPCO403_Lecture8.pdf`
- `GPCO 403 - Intl Econ - Handley/W4 - PPP, LOOP & Big Mac Application/Dollar-Denominated Public Debt in Asia and Latin America | St. Louis Fed.pdf`
- `GPCO 403 - Intl Econ - Handley/W5 - Midterm Review/Equations_Midterm_1.pdf`
- `GPCO 403 - Intl Econ - Handley/W5 - Midterm Review/Study Guide for GPCO 403 Midterm Spring 2025.pdf`
- `inbox/Intl Econ/GPCO403_Lecture4.pdf`
- `inbox/Intl Econ/GPCO403_Lecture6_20260415.pdf`
- `inbox/Intl Econ/GPCO403_Lecture6_20apr2026.pptx`
- `inbox/Intl Econ/GPCO403_Lecture7_PPP_22apr2026.pptx`
- `inbox/Intl Econ/International_Econ_Midterm2025_answerkey.pdf`
- `inbox/Intl Econ/Practice_questions.pdf`

## Verification

- Rebuilt with ReportLab using `build_midterm_theory_reference.py`.
- Verified with `pypdf`: 13 pages total.
- Verified structure: 1 cover/TOC page + 11 theory pages + 1 references/disclosure page.
- Verified PDF sidebar bookmarks: 11 outline entries, one for each theory.
- Verified TOC/link annotations: 11 annotations.
- Verified text extraction:
  - `GPT-5.5 (medium reasoning)` appears in the PDF provenance.
  - Generic `ChatGPT-5`, `GPT-5 via Codex`, and `GPT-5 via` strings do not appear.
  - ReportLab bold markup tags do not leak into extracted text.
  - Bullet extraction no longer includes control-character artifacts from the previous bullet glyph.

## Caveats

- This is a revision of the v1.0.0 study guide, not a fresh source rebuild. It keeps the v1.0.0 theory set and midterm calibration choices.
- Interest parity and crisis/regime material remain included because the Spring 2025 study guide and practice materials flag them as midterm-relevant; verify against any dedicated Spring 2026 midterm roadmap if Professor Handley posts one.

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5.5 (medium reasoning)
Sources: GPCO 403 course memory, existing study guides, v1.0.0 theory reference, Spring 2026 course folders, and `inbox/Intl Econ/` files listed above
Agent: Plutus
---
