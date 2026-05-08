# GPCO 403 Midterm Theory Reference v1.4.2 Notes

## Deliverable

- PDF: `GPCO 403_Midterm_Theory_Reference_v1.4.2.pdf`
- Matching notes: `GPCO 403_Midterm_Theory_Reference_v1.4.2_notes.md`
- Build script: `build_midterm_theory_reference.py`
- Conceptual image assets: `assets/gpco403_midterm_v1.4.0/`
- Date built: 2026-05-03
- Agent: Plutus and Hephaestus

## Revision Summary

Version 1.4.2 preserves the visible v1.4.1 PDF and notes unchanged. It keeps the same 11-theory midterm scope, same source/provenance conventions, and same visual assets, but moves the visuals out of the small main-page slot. Each theory page now has a compact pointer in the visual slot, followed immediately by a full enlarged visual page for that same theory.

Changes from v1.4.1:

1. Changed the output target from `v1.4.1` to `v1.4.2`; the v1.4.1 PDF and notes were not overwritten.
2. Replaced each small embedded main-page visual with a compact pointer to the next page.
3. Added one enlarged visual page after each of the 11 theory pages.
4. Preserved the four PNG conceptual assets from `assets/gpco403_midterm_v1.4.0/`.
5. Preserved the seven deterministic ReportLab diagrams as enlarged vector pages.
6. Kept model provenance as `GPT-5.5 (medium reasoning)`.
7. Preserved the builder overflow detector so clipped text fails the build.

## Verification

- Ran `python3 -m py_compile GPCO\ 403\ -\ Intl\ Econ\ -\ Handley/Study\ Guides/build_midterm_theory_reference.py`.
- Removed the incidental `Study Guides/__pycache__/` created by the compile check.
- Rebuilt with `python3 GPCO\ 403\ -\ Intl\ Econ\ -\ Handley/Study\ Guides/build_midterm_theory_reference.py`.
- Verified v1.4.1 remained present and unchanged as the visible prior artifact.
- Verified v1.4.2 generated as a separate PDF.
- Verified with `pdfinfo`: 24 pages total.
- Verified with `pypdf`:
  - v1.4.1 remains 13 pages.
  - v1.4.2 is 24 pages.
  - 22 outline entries: 11 theory entries and 11 nested visual entries.
  - 11 TOC link annotations remain on the cover page.
  - `VISUAL` appears 22 times, once in each main-page pointer and once in each enlarged visual page frame.
  - The main-page pointer appears 11 times.
  - `ELI5 CONCLUSION` appears 11 times.
  - `GPT-5.5 (medium reasoning)` appears in the PDF provenance.
  - Older generic model-provenance strings do not appear.
  - Embedded image XObjects appear on the four PNG visual pages: pages 3, 11, 17, and 23.
- Rendered all 11 visual pages with `pdftoppm` and checked the enlarged visual-region crops with Pillow; all rendered nonblank.

---
Generated for: Edgar Agunias
Date: 2026-05-03
Model: GPT-5.5 (medium reasoning)
Sources: v1.4.1 theory reference and notes; GPCO 403 course memory; existing Week 4 reference and Apr. 27 PPP/LOOP one-pager; Spring 2021 and 2025 midterm answer keys; practice questions; Lecture 6 and Lecture 7 PPP slides; Equations_Midterm_1 formula check; existing assets in `assets/gpco403_midterm_v1.4.0/`
Agent: Plutus; Hephaestus
---
