# Plutus — GPCO 403 Task Log

Record of major completed tasks. Read to avoid duplicate work.

<!-- No entries yet. Append new tasks below this line. -->

## 2026-04-15 — Data Brief 1 cross-check

Reviewed Edgar's `Data_Brief_1_Draft_Agunias.pdf` and `Data_Brief_1_Calculations_Companion.pdf` against assignment requirements. Wrote `Data Brief 1/crosscheck_plutus.md`.

Key findings:
- **Wrong data year.** Draft uses 2025 throughout; assignment requires 2024. Affects every Part A cell and every Part B numeric input.
- **Q2 sign flips under correct year.** Switching to 2024 figures (CA ≈ -2.1, Gov ≈ -1.8) makes Australia's private sector a small net borrower (-0.3%), not a net lender (+0.9%) as the draft says.
- **Q3 internal inconsistency.** Mixing IFS period-average rate (1.5520) with WEO-reported NGDPD ($1,829.5B) produces -8.73% rather than the clean -9.09% (= 1 − 1/1.10). Companion footnote acknowledges; Q3 prose does not.
- **Word count over.** Part B is 281 words, cap is 250.
- Q1 logic, Q3 direction, sources, units, and structure are all clean.

Estimated as-is grade: 2/5. Post-fix estimate: 5/5. Fix time: 30 to 45 minutes.

## 2026-04-15 — Data Brief 1 FINAL produced

Produced submission-ready corrected version addressing every P0-P2 item from my own crosscheck.

**Deliverables:**
- `Data Brief 1/Data_Brief_1_FINAL_Agunias.pdf` (single-page PDF, ReportLab-generated)
- `Data Brief 1/Data_Brief_1_FINAL_Agunias.md` (Markdown source for Google Doc paste-in if needed)
- Original `Data_Brief_1_Draft_Agunias.pdf` left untouched as backup.

**Changes vs. draft:**
- All Part A cells re-pulled to 2024 targets from WEO October 2025 release: AU GDP $1,778B USD / A$2,693B / $65,373 per capita / CA -2.1% / Gov -1.8%; US GDP $29,184B / $86,601 per capita / CA -3.9% / Gov -7.6%. AUD/USD IFS period-average 1.5167.
- Q2 conclusion flipped from "net lender (+0.9%)" to "small net borrower (-0.3%)" under 2024 numbers.
- Q3 switched to WEO-implied rate (1.5146) for internal consistency, showing new rate 1.6661, new GDP USD $1,616.4B, -9.09% (clean 1/1.10 result). One sentence flags the methodology choice in the sources note.
- Part B trimmed from 281 to 220 words.
- Title deemdashed ("Data Brief 1: Australia vs. United States (2024)") per Edgar's writing style rules.
- AI Use Disclosure block added (Variant C, moderate use — data cross-check, line edit, formatting).

**Estimated grade:** 5/5.

**Open methodology note for Edgar:** The IFS rate (1.5167) and WEO-implied rate (1.5146) differ by 0.14%. I kept the IFS rate in the table for source discipline and explicitly used the WEO-implied rate in Q3 for arithmetic consistency. The source footnote under the table discloses this choice so a strict grader can see the reasoning.

## 2026-04-15 — Data Brief 1 "Farm-to-Table" Companion produced

Built a teaching-style walkthrough companion for Edgar's own learning, tied to the FINAL submission (2024 data). Saved as `Data Brief 1/Data_Brief_1_FINAL_Companion.md`.

**Structure (8 sections):**
1. The Two Data Sources (WEO and IFS) with release cadence, navigation paths, series codes
2. The Variables — full ingredient table mapping every Part A row to its series code and plain-English meaning
3. Exchange Rate Reconciliation — IFS 1.5167 vs WEO-implied 1.5146, why they differ, why Q3 uses the WEO-implied rate
4. Q1 walkthrough — living standards intuition, PPP limitation, 75.5% ratio derivation
5. Q2 walkthrough — sectoral balances identity with full minus-minus sign explanation
6. Q3 walkthrough — pass-through algebra showing why a 10% depreciation produces -9.09% not -10%
7. Reproducibility Checklist — step-by-step to pull every number cold
8. Concept Glossary — plain-English definitions for every macro term used

**Word count:** ~4,527 words. Markdown only (no PDF render).

**Study takeaway captured in the doc:** Wrong year, right formula still fails. The Q2 sign flip between draft and final came purely from a year-filter mistake. Future data briefs should start by writing the target year at the top of the scratchpad before touching a database.

## 2026-04-16 — Week 4 Reference Manual (LOOP, PPP, Real FX)

Built `Study Guides/GPCO 403_Week_4_Reference.pdf` covering the Week 4 folder material (Lecture 8: Law of One Price, Purchasing Power Parity, Real Exchange Rate, Big Mac Index, Currency Supply & Demand) plus the supplementary St. Louis Fed dollar-denominated-debt reading. Skills applied: `lecture-to-reference-pdf` (three-layer rule, decoder, copy-paste blocks, period-awareness callouts, hyperlinked TOC) and `pdf` (ReportLab build + pypdf Link annotations).

**Deliverable:** `Study Guides/GPCO 403_Week_4_Reference.pdf`, 22 pages, 19 sections, all TOC entries hyperlinked to their destination pages. Single-file manual ready to carry into Wednesday lecture and the May 4 midterm (LOOP and PPP sections are on-midterm; currency supply-demand material flagged as final-only per Lecture 8 slide 39).

**Structure:**
1. Concept Map and Week 4 at a Glance (includes midterm vs final scope flag)
2-5. LOOP, Big Mac Index, why LOOP fails, arbitrage band with trade cost tau
6-9. Absolute PPP, Real Exchange Rate, Relative PPP derivation, over/under-valued currencies
10-12. Currency Supply & Demand (final-exam material), shifters, "never reason from a price change" with Australia iron-ore case
13. Empirical evidence: Crucini, Telmer, Zachariadis (2005)
14. Supplementary: dollar-denominated debt and FX risk
15. Copy-paste formula blocks (4 Excel-ready blocks: LOOP/PPP checks, relative PPP, Big Mac Index, arbitrage band)
16. Abbreviation/symbol decoder (16 entries)
17. Exam question type guide (five canonical shapes with solution procedures)
18. Data Brief 1 connections (sectoral balances linked to FX S&D; pass-through linked to tradables share; Australia commodity exposure linked to "never reason from a price change")
19. Attribution and output disclosure

**Build notes worth remembering for future PDFs:**
- Registered Arial Unicode TTF (`/System/Library/Fonts/Supplemental/Arial Unicode.ttf`) via `pdfmetrics.registerFont(TTFont(...))` to get clean Greek letters and math symbols. Default Helvetica rendered Δ π τ Σ ≤ → as broken glyphs or "fi"/"p"/"£" ligature artifacts — every future reference PDF with math content needs Unicode font registration.
- Used `<cell>` style placeholders in copy-paste blocks caused ReportLab's Paragraph tag parser to strip the placeholder text. Switched to `[bracket]` style. Standard lesson: anything inside `<>` in a Paragraph gets parsed as markup.
- TrackingDoc + pypdf Link annotation pattern from the skill worked cleanly: 19/19 TOC entries mapped to their sections on first assembly.

**Known limitations:**
- Per the folder name "W4 - PPP, LOOP & Big Mac Application", I treated the Lecture 8 material as Week 4 content. The syllabus course grid lists PPP/LOOP/Big Mac under Week 5, so Professor Handley may have reorganized between the posted syllabus and the current folder structure. The material itself is unambiguous; the week label is the only thing in flux.
- If additional Week 4 readings or supplementary notes drop on Canvas after 2026-04-16, they are not yet reflected.
