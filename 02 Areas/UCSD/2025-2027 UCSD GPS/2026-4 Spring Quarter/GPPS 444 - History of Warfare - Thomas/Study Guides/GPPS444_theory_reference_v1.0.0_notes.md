# GPPS 444 Theory Reference v1.0.0 - Source Notes

## Deliverable

- PDF: `GPPS444_theory_reference_v1.0.0.pdf`
- Generator: `build_gpps444_theory_reference_v1.0.0.py`
- Assets: `assets/gpps444_theory_reference_v1.0.0/`
- Verification renders: `_verification_gpps444_theory_reference_v1.0.0/`

## Source Inventory

Primary starting point was the existing midterm/reference work:

- `Study Guides/GPPS_444_Midterm_Framework_Reference_v1.1.1.pdf`
- `Study Guides/GPPS_444_Midterm_Framework_Reference_v1.1.1_notes.md`
- `Study Guides/build_midterm_framework_reference_v1.1.1.py`
- `.archive/midterm_framework_reference/` for prior versions

Course-order and source list were checked against:

- `Course Admin/syllabus_extracted.md`
- `Course Admin/GPPS 444 (HOW) S26.pdf`
- `Readings/The Cambridge History of Warfare -- Geoffrey Parker -- 2020 -- Cambridge University Press.pdf`
- `Study Guides/ch5_new_weapons_new_tactics_1pager.md`
- `Study Guides/chevauchee_explainer.md`
- `Study Guides/session8_ottoman_expansion_dynastic_war_1pager.md`
- `Study Guides/session9_napoleonic_wars_i_nations_in_arms_1pager.md`
- `Study Guides/session10_napoleonic_wars_ii_1pager.md`
- `Study Guides/2026-05-11_session13_mechanized_warfare_ii_wwi_1pager.md`
- `Study Guides/2026-05-13_murray_world_in_conflict_1pager.md`
- `Study Guides/2026-05-18_session15_undersea_air_sea_battle_wwii_1pager.md`
- `Study Guides/2026-05-20_session16_sea_land_battle_wwii_1pager.md`
- `Study Guides/2026-05-27_sessions17-20_nuclear_weapons_and_future_warfare_1pager.md`
- `_agent/BATTLE_NOTES/TCHW_Epilogue_Future_of_Warfare.md`
- `_agent/AGENT_CONTEXT.md`
- `_agent/FEEDBACK.md`

## Theory Inventory In Syllabus Order

1. Thomas Battle-Outcome Framework
2. Western Way of War
3. Hoplite-Phalanx Citizen Soldier Model
4. Roman Adaptability and Engineering
5. Castle, Fortress, and Siege Dominance
6. Chevauchee and Economic Warfare
7. Infantry, Missile, and Polearm Revolution
8. Gunpowder Revolution and Trace Italienne
9. Ottoman Expansion and Standing Military Institutions
10. Dynastic War, Volley Fire, and Combined Arms
11. Nation in Arms and Napoleonic Operational System
12. Limits of Mass, Mobility, and Coalition War
13. Industrialization of War, 1815-1871
14. Towards World War I: Firepower and Stalemate
15. WWI Adaptation, Air Power, and Combined Arms
16. WWII Air-Land Battle and Blitzkrieg
17. Undersea and Air-Sea Battle
18. Amphibious and Airborne Operational Learning
19. Nuclear Weapons and Modern Strategy
20. Revolution in Military Affairs and Precision Warfare
21. Asymmetric Warfare and Demodernization
22. Future Warfare: Space, AI, and Network Fragility

## Image Method

The runtime produced course-local explanatory mechanism diagrams with PIL rather than remote image generation. Each diagram follows the theory-image SOP by teaching mechanism rather than decorating: four low-density labels, a mechanism box, and a caption in the PDF mapping mechanism, assumption, and strength/limit cue.

## Verification

- Ran `python3 build_gpps444_theory_reference_v1.0.0.py` from `Study Guides/`.
- PDF generated successfully: `GPPS444_theory_reference_v1.0.0.pdf`.
- PyMuPDF verification:
  - 46 pages total.
  - 23 outline entries: 22 theory bookmarks plus references/disclosure.
  - 22 pages contain embedded images.
  - Text extraction found 22 instances each of `SITUATION`, `CORE INTUITION`, `KEY CONCEPTS`, `ASSUMPTIONS`, and `APA REFERENCES / UNIT DISCLOSURE`.
- Rendered all 46 pages to `_verification_gpps444_theory_reference_v1.0.0/`.
- Contact sheet reviewed visually; no blank pages or obvious layout overflow observed.

## Known Limits

- Sessions 11 and 12 did not have local one-pagers visible in `Study Guides/`, so those units were synthesized from the syllabus order and TCHW chapter sequence rather than a prior Ares one-pager.
- The syllabus/textbook edition mismatch remains important: the local PDF table of contents shows the source as the 2005 revised TCHW text in metadata/pages, while the course memory and syllabus use the 2020/2nd-edition label. The PDF keeps the course-facing 2020/Parker convention where prior course materials use it, but individual chapter references follow the local PDF's revised-edition chapter/page pattern used in existing Ares notes.

---
Generated for: Edgar Agunias
Date: 2026-05-31
Model: GPT-5 Codex
Sources: GPPS 444 syllabus extraction, Parker/TCHW PDF, existing midterm framework reference v1.1.1, session one-pagers, Ares memory files
Agent: Ares
---
