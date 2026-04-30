# GPPS 444 Midterm Framework Reference v1.1.0 - Source Notes

## Deliverable

- PDF: `GPPS_444_Midterm_Framework_Reference_v1.1.0.pdf`
- Generator: `build_midterm_framework_reference_v1.1.0.py`
- Prior version preserved unchanged: `GPPS_444_Midterm_Framework_Reference.pdf`, `GPPS_444_Midterm_Framework_Reference_notes.md`, and `build_midterm_framework_reference.py`
- Purpose: update the midterm framework reference to the new reference-sheet standard by adding compact conceptual visual slots, graph statements, planned imagegen asset paths, and ELI5 conclusions for each major framework.

## Version Decision

The existing reference was unversioned but already a complete first release. This update is `v1.1.0` rather than `v1.0.1` because it adds a substantive document pattern, not just typo, citation, or formatting cleanup.

## Method

Started from the existing builder and created a versioned successor. The framework content, source base, ordering, APA references, PDF bookmarks, and hyperlinked table of contents remain aligned with the original reference. Version 1.1.0 adds a compact visual-planning slot to each framework page:

- `CONCEPTUAL GRAPH` - a one-line causal schematic for quick recall.
- `IMAGEGEN SLOT` - a planned asset path and concrete prompt if Edgar later wants bitmap visuals.
- `ELI5 CONCLUSION` - a short plain-language final takeaway for the framework.

No bitmap image assets were generated or embedded in this pass. The PDF implements the visual standard as readable prompt/graph slots so the reference is usable immediately and image generation can be done later without blocking.

## Imagegen Prompt List and Planned Asset Paths

1. `assets/midterm_framework_reference_v1.1.0/01_thomas_battle_analysis.png`
   Prompt: Create a clean conceptual study-guide diagram for a History of Warfare midterm: central node "Battle Outcome" surrounded by mass, mobility, adaptability, logistics, leadership, terrain, weather, technology, organization, and chance; restrained academic style, navy/gold/green palette, readable labels, no photorealistic soldiers, 16:9.

2. `assets/midterm_framework_reference_v1.1.0/02_western_way_war.png`
   Prompt: Create a conceptual timeline-map for "Western Way of War": disciplined infantry, decisive battle, state finance, technology, and institutional learning flowing from ancient formations to early modern armies; include a caution label "not a simple superiority story"; academic reference-sheet style, 16:9.

3. `assets/midterm_framework_reference_v1.1.0/03_hoplite_phalanx.png`
   Prompt: Create a simple overhead conceptual diagram of a hoplite phalanx holding a narrow pass against a larger force: show frontage, shield wall cohesion, restricted terrain, and mass being compressed; no gore, clean labels, navy/gold/stone palette, 16:9.

4. `assets/midterm_framework_reference_v1.1.0/04_roman_adaptation.png`
   Prompt: Create a conceptual cycle diagram for Roman warfare: defeat, adaptation, flexible legion, road/camp/siege engineering, expansion, and political strain; include small icons for road, camp, wall, and legion block; sober academic style, 16:9.

5. `assets/midterm_framework_reference_v1.1.0/05_fortress_siege.png`
   Prompt: Create a conceptual siege diagram: a castle or fortress controlling routes and nearby population, with attacker costs labeled time, labor, food, engineering, and negotiation; emphasize defense dominance, clean medieval map style, 16:9.

6. `assets/midterm_framework_reference_v1.1.0/06_chevauchee.png`
   Prompt: Create a conceptual route map of a medieval chevauchee: a fast mounted raid moving around castles, burning tax base icons, forcing a ruler into a dilemma "fight badly or look weak"; no gore, restrained study-guide palette, 16:9.

7. `assets/midterm_framework_reference_v1.1.0/07_infantry_revolution.png`
   Prompt: Create a clean battlefield concept diagram for late medieval infantry tactics: longbowmen, stakes, mud/prepared ground, pikes or polearms, and mounted knights losing shock power; emphasize tactics plus terrain over weapon alone, 16:9.

8. `assets/midterm_framework_reference_v1.1.0/08_gunpowder_trace.png`
   Prompt: Create a three-step conceptual graphic for the gunpowder revolution: old high wall cracked by cannon, trace italienne bastion absorbing and flanking fire, fiscal-military state paying for bigger sieges; readable labels, academic navy/gold palette, 16:9.

9. `assets/midterm_framework_reference_v1.1.0/09_ottoman_standing.png`
   Prompt: Create a respectful conceptual diagram of Ottoman early modern military power: Janissary standing infantry, siege artillery, imperial logistics, and Habsburg-Ottoman frontier fortresses; avoid stereotypes, use clean map-and-icons style, 16:9.

10. `assets/midterm_framework_reference_v1.1.0/10_dynastic_firepower.png`
    Prompt: Create a conceptual combined-arms diagram for Breitenfeld 1631: Swedish flexible formations, volley fire, regimental artillery, cavalry support, and deeper Imperial tercio-style formations; clean labels, no gore, 16:9.

11. `assets/midterm_framework_reference_v1.1.0/11_nation_in_arms.png`
    Prompt: Create a conceptual operational map for Napoleon's system: national manpower feeding corps columns that march separately and concentrate at Austerlitz; include deception, artillery, and command nodes; clean academic reference style, 16:9.

12. `assets/midterm_framework_reference_v1.1.0/12_napoleonic_limits.png`
    Prompt: Create a conceptual failure-chain diagram for Napoleon's limits: corps mobility stretching into Russia, scorched earth, winter/weather, long supply line, coalition learning, and Waterloo coalition pressure; sober study-guide style, 16:9.

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
- Existing `GPPS_444_Midterm_Framework_Reference_notes.md`
- Existing `build_midterm_framework_reference.py`

## Verification

- Ran `python3 build_midterm_framework_reference_v1.1.0.py` from the Study Guides folder.
- Verified with `pypdf`: `GPPS_444_Midterm_Framework_Reference_v1.1.0.pdf` has 14 pages and 12 sidebar outline entries.
- Verified extracted PDF text contains 12 `CONCEPTUAL GRAPH` slots, 12 `IMAGEGEN SLOT` slots, 12 planned asset paths, and 12 `ELI5 CONCLUSION` blocks.
- Confirmed the original unversioned PDF, notes, and builder timestamps were not changed.

---
Generated for: Edgar Agunias
Date: 2026-04-30
Model: GPT-5 Codex
Sources: Ares memory; existing GPPS 444 midterm framework reference notes and builder; Claudia SOPs and theory-reference-pdf skill
Agent: Ares
---
