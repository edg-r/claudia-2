# GPPS 444 Midterm Framework Reference v1.1.1 - Source Notes

## Deliverable

- PDF: `GPPS_444_Midterm_Framework_Reference_v1.1.1.pdf`
- Generator: `build_midterm_framework_reference_v1.1.1.py`
- Prior versions preserved unchanged: `GPPS_444_Midterm_Framework_Reference.pdf`, `GPPS_444_Midterm_Framework_Reference_notes.md`, `build_midterm_framework_reference.py`, `GPPS_444_Midterm_Framework_Reference_v1.1.0.pdf`, `GPPS_444_Midterm_Framework_Reference_v1.1.0_notes.md`, and `build_midterm_framework_reference_v1.1.0.py`
- Purpose: integrate the 12 completed PNG assets into the midterm framework reference while preserving the v1.1.0 text architecture, graph statements, and ELI5 conclusions.

## Version Decision

The existing reference was unversioned but already a complete first release. Version `v1.1.0` added the visual-slot architecture. This update is `v1.1.1` because it is a patch-level asset integration: same framework content and page architecture, now with the actual images embedded.

## Method

Started from the v1.1.0 builder and created a versioned successor. The framework content, source base, ordering, APA references, PDF bookmarks, and hyperlinked table of contents remain aligned with the original reference. Version 1.1.1 replaces each planned imagegen slot with the completed PNG asset:

- `CONCEPTUAL GRAPH` - a one-line causal schematic for quick recall.
- Embedded image - the corresponding completed PNG from `assets/midterm_framework_reference_v1.1.0/`.
- `ELI5 CONCLUSION` - a short plain-language final takeaway for the framework.

No unrelated session one-pagers were edited. The original unversioned reference and v1.1.0 reference were preserved.

## Embedded Asset List

1. `assets/midterm_framework_reference_v1.1.0/01_battle_outcome_framework.png`
2. `assets/midterm_framework_reference_v1.1.0/02_western_way_of_war.png`
3. `assets/midterm_framework_reference_v1.1.0/03_hoplite_phalanx_terrain.png`
4. `assets/midterm_framework_reference_v1.1.0/04_roman_adaptation_cycle.png`
5. `assets/midterm_framework_reference_v1.1.0/05_medieval_siege_defense.png`
6. `assets/midterm_framework_reference_v1.1.0/06_chevauchee_route_map.png`
7. `assets/midterm_framework_reference_v1.1.0/07_late_medieval_infantry_tactics.png`
8. `assets/midterm_framework_reference_v1.1.0/08_gunpowder_trace.png`
9. `assets/midterm_framework_reference_v1.1.0/09_ottoman_standing.png`
10. `assets/midterm_framework_reference_v1.1.0/10_dynastic_firepower.png`
11. `assets/midterm_framework_reference_v1.1.0/11_nation_in_arms.png`
12. `assets/midterm_framework_reference_v1.1.0/12_napoleonic_limits.png`

## Sources Used

- `AGENTS.md`
- `_claudia/system/CLAUDIA.md`
- `_claudia/system/manifest.json`
- `_claudia/system/CODEX_WORKFLOW.md`
- All SOPs in `_claudia/sop/`
- `_claudia/skills/theory-reference-pdf.md`
- `_claudia/agent_definitions/ares.md`
- `GPPS 444 - History of Warfare - Thomas/_agent/AGENT_CONTEXT.md`
- `GPPS 444 - History of Warfare - Thomas/_agent/FEEDBACK.md`
- Existing `GPPS_444_Midterm_Framework_Reference_v1.1.0_notes.md`
- Existing `build_midterm_framework_reference_v1.1.0.py`
- 12 PNG files in `assets/midterm_framework_reference_v1.1.0/`

## Verification

- Ran `python3 build_midterm_framework_reference_v1.1.1.py` from the Study Guides folder.
- Verified with `pypdf`: `GPPS_444_Midterm_Framework_Reference_v1.1.1.pdf` has 14 pages, 12 sidebar outline entries, and 12 embedded image XObjects.
- Verified page distribution: pages 2-13 each contain 1 embedded image; cover and references pages contain 0 images.
- Verified extracted PDF text contains 12 `CONCEPTUAL GRAPH` blocks and 12 `ELI5 CONCLUSION` blocks.
- Rendered all 14 pages with PyMuPDF into `_verification_v1.1.1/`; page image statistics confirm nonblank pages, and contact-sheet review showed no obvious overflow or missing visual slots.
- Confirmed the original unversioned PDF/builder and v1.1.0 PDF/builder were preserved unchanged.

---
Generated for: Edgar Agunias
Date: 2026-04-30
Model: GPT-5 Codex
Sources: Ares memory; existing GPPS 444 midterm framework v1.1.0 notes and builder; 12 PNG assets; Claudia SOPs and theory-reference-pdf skill
Agent: Ares
---
