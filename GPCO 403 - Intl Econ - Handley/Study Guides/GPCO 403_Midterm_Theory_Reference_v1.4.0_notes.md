# GPCO 403 Midterm Theory Reference v1.4.0 Notes

## Deliverable

- PDF: `GPCO 403_Midterm_Theory_Reference_v1.4.0.pdf`
- Matching notes: `GPCO 403_Midterm_Theory_Reference_v1.4.0_notes.md`
- Build script: `build_midterm_theory_reference.py`
- Conceptual asset markers: `assets/gpco403_midterm_v1.4.0/`
- Date built: 2026-04-30
- Agent: Plutus

## Revision Summary

Version 1.4.0 preserves v1.3.0 unchanged and keeps the same 11-theory midterm scope. It adds code-generated diagrams directly in the ReportLab builder for exact economics visuals, and it adds an ELI5 conclusion box to every theory page.

Changes from v1.3.0:

1. Changed the output target from `v1.3.0` to `v1.4.0`; the v1.3.0 PDF and notes were not overwritten.
2. Added deterministic canvas-drawn diagrams for all 11 theory pages.
3. Added ELI5 conclusion boxes that translate each page into a final plain-English takeaway.
4. Added PDF-visible imagegen markers on the pages where a future conceptual visual would be useful.
5. Created `assets/gpco403_midterm_v1.4.0/` with placeholder briefs for the imagegen-needed conceptual slots.
6. Preserved the builder overflow detector so clipped text fails the build.
7. Kept model provenance as `GPT-5.5 (medium reasoning)`.

## Deterministic Graphs Added

- National income accounting: value-added/final-output flow.
- Balance of payments: current-account deficit matched by financial-account surplus.
- Savings-investment gap: bar comparison showing `I > S` and foreign financing.
- External wealth: stock path showing CA flows plus valuation changes.
- Intertemporal trade: two-period borrowing and repayment timeline.
- Cross-rate arbitrage: triangular USD-JPY-MXN loop.
- Interest parity: home return versus covered foreign return.
- Crisis balance sheets: local revenues versus dollar debt after depreciation.
- Law of one price: no-arbitrage band.
- PPP and real exchange rate: real exchange-rate path around a long-run anchor.
- Big Mac Index: common-currency / market-FX / PPP-FX comparison bars.

## Imagegen Placeholders Still Needed

These are optional conceptual upgrades, not blockers for v1.4.0 usefulness. Placeholder briefs live in the asset folder:

1. `global_supply_chain_gdp_cutaway.md`
2. `consumption_smoothing_bridge.md`
3. `dollar_debt_balance_sheet_scene.md`
4. `big_mac_ppp_market_scene.md`

## Verification

- Rebuilt with `python3 GPCO\ 403\ -\ Intl\ Econ\ -\ Handley/Study\ Guides/build_midterm_theory_reference.py`.
- Builder overflow detector completed cleanly.
- Verified v1.3.0 PDF remained present and was not overwritten.
- Verified v1.4.0 is generated as a separate PDF.
- Verified with `pypdf`: 13 pages total.
- Verified PDF sidebar bookmarks: 11 outline entries, one for each theory.
- Verified TOC/link annotations: 11 annotations.
- Verified text extraction:
  - `VISUAL` appears 11 times.
  - `ELI5 CONCLUSION` appears 11 times.
  - `Imagegen marker` appears 4 times.
  - `GPT-5.5 (medium reasoning)` appears in the PDF provenance.
  - Older generic model-provenance strings do not appear.
- Rendered page 2 with `pdftoppm` and inspected the output image for visual layout sanity.

---
Generated for: Edgar Agunias
Date: 2026-04-30
Model: GPT-5.5 (medium reasoning)
Sources: v1.3.0 theory reference and notes; GPCO 403 course memory; existing Week 4 reference and Apr. 27 PPP/LOOP one-pager; Spring 2021 and 2025 midterm answer keys; practice questions; Lecture 6 and Lecture 7 PPP slides; Equations_Midterm_1 formula check
Agent: Plutus
---
