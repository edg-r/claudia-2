# GPCO 403 Midterm Theory Reference v1.4.1 Notes

## Deliverable

- PDF: `GPCO 403_Midterm_Theory_Reference_v1.4.1.pdf`
- Matching notes: `GPCO 403_Midterm_Theory_Reference_v1.4.1_notes.md`
- Build script: `build_midterm_theory_reference.py`
- Conceptual image assets: `assets/gpco403_midterm_v1.4.0/`
- Date built: 2026-04-30
- Agent: Plutus

## Revision Summary

Version 1.4.1 preserves v1.3.0 and v1.4.0 unchanged and keeps the same 11-theory midterm scope. It embeds the four finished conceptual PNGs in the visual slots that v1.4.0 marked for imagegen upgrades, while leaving the other seven deterministic ReportLab diagrams and all ELI5 conclusion boxes in place.

Changes from v1.4.0:

1. Changed the output target from `v1.4.0` to `v1.4.1`; the v1.3.0 and v1.4.0 PDFs and notes were not overwritten.
2. Added ReportLab image embedding with aspect-fit sizing inside the existing `VISUAL` frame.
3. Embedded `gdp_supply_chain_cutaway.png` on the National Income Accounting and Open-Economy GDP page.
4. Embedded `consumption_smoothing_bridge.png` on the Intertemporal Trade and Consumption Smoothing page.
5. Embedded `dollar_debt_balance_sheet_scene.png` on the Exchange-Rate Regimes and Crisis Balance Sheets page.
6. Embedded `big_mac_ppp_market_scene.png` on the Big Mac Index as Applied PPP page.
7. Removed the PDF-visible imagegen marker text from the four upgraded pages.
8. Preserved the builder overflow detector so clipped text fails the build.
9. Kept model provenance as `GPT-5.5 (medium reasoning)`.

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

## Embedded Conceptual PNGs

These now appear in the patch-version PDF:

1. `gdp_supply_chain_cutaway.png`
2. `consumption_smoothing_bridge.png`
3. `dollar_debt_balance_sheet_scene.png`
4. `big_mac_ppp_market_scene.png`

## Verification

- Rebuilt with `python3 GPCO\ 403\ -\ Intl\ Econ\ -\ Handley/Study\ Guides/build_midterm_theory_reference.py`.
- Builder overflow detector completed cleanly.
- Verified v1.3.0 PDF remained present and was not overwritten.
- Verified v1.4.0 PDF remained present and was not overwritten.
- Verified v1.4.1 is generated as a separate PDF.
- Verified with `pypdf`: 13 pages total.
- Verified PDF sidebar bookmarks: 11 outline entries, one for each theory.
- Verified TOC/link annotations: 11 annotations.
- Verified text extraction:
  - `VISUAL` appears 11 times.
  - `ELI5 CONCLUSION` appears 11 times.
  - `Imagegen marker` appears 0 times.
  - `GPT-5.5 (medium reasoning)` appears in the PDF provenance.
  - Older generic model-provenance strings do not appear.
- Verified embedded PDF image XObjects with `pypdf`.
- Rendered the four upgraded pages with `pdftoppm` and checked nonblank crop statistics with Pillow.
- Verified each upgraded page had nonblank pixels in the visual region and no builder-reported overflow.

---
Generated for: Edgar Agunias
Date: 2026-04-30
Model: GPT-5.5 (medium reasoning)
Sources: v1.3.0 theory reference and notes; GPCO 403 course memory; existing Week 4 reference and Apr. 27 PPP/LOOP one-pager; Spring 2021 and 2025 midterm answer keys; practice questions; Lecture 6 and Lecture 7 PPP slides; Equations_Midterm_1 formula check
Agent: Plutus
---
