# GPCO 403 Comprehensive Theory Reference v1.1.0 Notes

## Inventory

Built from the visible midterm theory reference v1.4.2 and post-midterm study guides/readings in syllabus order.

1. Weeks 1-2 - National Income Accounting and Open-Economy GDP - International Economics, Ch. 16, Sections 16.1-16.3; GPCO 403 Lectures 1-2
2. Week 2 - Current Account and Balance of Payments Identity - International Economics, Ch. 12, Section 12.2 and Ch. 16, Sections 16.3-16.5; GPCO 403 Lecture 3
3. Week 2 - Savings-Investment Gap and Twin Deficits - International Economics, Ch. 16, Section 16.4; GPCO 403 Lecture 3
4. Weeks 3-4 - External Wealth and Valuation Effects - International Economics, Ch. 17, Section 17.1; GPCO 403 Lectures 4 and 6
5. Week 4 - Intertemporal Trade and Consumption Smoothing - International Economics, Ch. 17, Section 17.1; GPCO 403 Lecture 6
6. Week 3 - Exchange-Rate Basics and Cross-Rate Arbitrage - International Economics, Ch. 12, Section 12.1; GPCO 403 Lecture 6 and Lecture 7 PPP Slides
7. Week 3 - Interest Parity and Forward Exchange Rates - International Economics, Ch. 13, Sections 13.1-13.4; Study Guide for GPCO 403 Midterm Spring 2025
8. Week 5 - Exchange-Rate Regimes and Crisis Balance Sheets - Study Guide for GPCO 403 Midterm Spring 2025; GPCO 403 Lecture 6; Dollar-Denominated Public Debt in Asia and Latin America
9. Week 5 - Law of One Price - International Economics, Ch. 14, Section 14.1; GPCO 403 Lectures 7-8; GPCO 403 Week 4 Reference
10. Week 5 - Purchasing Power Parity and the Real Exchange Rate - International Economics, Ch. 14, Section 14.1; GPCO 403 Lectures 7-8; GPCO 403 Week 4 Reference
11. Week 5 - Big Mac Index as Applied PPP - The Big Mac Index; 2026-04-27 PPP, LOOP, and Big Mac One-Page Summary; GPCO 403 Week 4 Reference
12. Week 6 - Ricardian Comparative Advantage - International Economics, Ch. 2; The Economist, The Miracle of Trade; Ricardian practice problems
13. Week 7 - Heckscher-Ohlin Factor Endowments - International Economics, Ch. 4 and Ch. 17.1; Heckscher-Ohlin one-pager
14. Week 7 - Stolper-Samuelson Distributional Effects - International Economics, Ch. 4; Concept Check 4 prep
15. Week 7 - Factor Price Equalization and Its Limits - International Economics, Ch. 4; Heckscher-Ohlin practice questions
16. Week 8 - Increasing Returns and Monopolistic Competition - International Economics, Ch. 6; firms and increasing returns one-pager
17. Week 8 - Firm Heterogeneity and Export Selection - International Economics, Ch. 6; firms and increasing returns class prep
18. Week 9 - Small-Country Tariff Welfare - International Economics, Ch. 8; Week 9 trade policy prep
19. Week 9 - Large-Country Tariff and Optimal Tariff Logic - International Economics, Ch. 8; Week 9 trade policy prep
20. Week 9 - Import Quotas and Voluntary Export Restraints - International Economics, Ch. 8; Week 9 trade policy prep
21. Week 9 - GATT/WTO Cooperation, MFN, and National Treatment - International Economics, Ch. 11.1-11.2; Week 9 trade policy prep
22. Week 9 - Preferential Trade Agreements, Trade Creation, and Trade Diversion - International Economics, Ch. 11.2; Week 9 trade policy prep; Viner's PTA framework
23. Week 9 - 2018 Tariffs, Pass-Through, and Welfare Evidence - Amiti, Redding, and Weinstein, The Impact of the 2018 Tariffs on Prices and Welfare; Week 9 prep

## Source Status

- Weeks 1-9 have assigned readings recorded in Plutus READINGS.md and syllabus_extracted.md.
- Week 10 is listed in the local syllabus extraction as Trade Policy II / final roadmap with no new reading separately assigned.
- No separate Weeks 10-11 reading files were present in the course folder at build time.

## Output

- PDF: `GPCO403_theory_reference_v1.1.0.pdf`
- Builder: `build_gpco403_theory_reference_v1.1.0.py`
- Assets: `assets/gpco403_theory_reference_v1.1.0/`

## Revision Summary from v1.0.0

- Preserved the 47-page, two-pages-per-theory architecture: one theory page plus one immediately paired visual/reference page for each of 23 theories.
- Expanded every theory page with deeper mechanism, why-it-works, when-assumptions-fail, exam-use, and author/textbook example blocks.
- Added a bottom synthesis strip to every theory page: contrast, common trap, and diagnostic question.
- Expanded every visual/reference page with visual reading checks and a fast application prompt so the second page functions as a study page, not just an image/citation page.
- Kept all visual assets in the project-bound v1.1.0 asset folder and retained one PNG explainer per theory.

## Verification Targets

- Expected page count: 47 pages.
- Expected theory units: 23.
- Each theory has one PNG explainer asset and two PDF pages.
- TOC entries and PDF sidebar bookmarks are generated.

## Verification Results

- `pypdf` page count: 47 pages.
- `pypdf` sidebar outline/bookmarks: 46 entries, covering 23 theory pages and 23 nested visual pages.
- TOC link annotations: 23.
- Required text-page sections present 23 times each: mechanism, why it works, when assumptions fail, exam use, author/textbook example, contrast, common trap, diagnostic question.
- Required visual-page sections present 23 times each: caption/footnote, APA references, unit disclosure, visual reading checks, fast application.
- Image XObjects: 23 pages with images, 23 total images.
- Provenance check: exact `GPT-5.5 (medium reasoning)` present; stale generic `GPT-5 via Codex` / `ChatGPT-5` strings absent.
- Render check: all 47 pages rendered via `pdftoppm`; cover is the only intentionally light page by pixel-density proxy; sampled pages 2, 3, 34, and 47 showed readable layout with no overlap.
- Density comparison by extracted text: v1.0.0 theory pages averaged about 2,670 characters; v1.1.0 theory pages average about 4,026 characters. v1.0.0 visual/reference pages averaged about 978 characters; v1.1.0 visual/reference pages average about 1,423 characters.

---
Generated for: Edgar Agunias
Date: 2026-06-01
Model: GPT-5.5 (medium reasoning)
Sources: GPCO 403 syllabus extraction, Plutus memory files, existing midterm theory reference builder/notes, and post-midterm study guides/readings
Agent: Plutus
---
