# GPPS 463 Midterm Theory Reference v1.3.0 -- Source Notes

## Purpose

This notes file documents the v1.3.0 revision of `GPPS_463_Midterm_Theory_Reference_v1.3.0.pdf`. The revision preserves v1.2.0 unchanged and updates `build_midterm_theory_reference.py` as the current builder for the new reference-sheet standard.

## Revision Scope

- Bumped the builder output from v1.2.0 to v1.3.0.
- Added a `CONCEPTUAL VISUAL SLOT` section to each major theory/topic.
- Added a short `ELI5 CONCLUSION` section to each major theory/topic.
- Kept the existing 11-framework scope and the v1.2.0 two-page spread structure.
- Did not generate actual image assets in this pass. The PDF and notes provide concrete imagegen prompts plus target asset paths for later generation.
- Corrected v1.3.0 provenance to `GPT-5 via Codex (reasoning effort not exposed)`. The source base still includes earlier v1.2.0 work that reported `GPT-5.5 (medium reasoning)`.

## Imagegen Prompt List and Asset Paths

1. Constructed region
   - Asset path: `Study Guides/assets/midterm_theory_reference_v1.3.0/constructed_region_shared_experience_map.png`
   - Graph logic: Concept map: diversity nodes feeding into shared regional category and ASEAN/Cold War institutionalization.
   - Prompt: Create a clean editorial concept-map graphic for a graduate study guide. Show Southeast Asia as a constructed political region, not a natural cultural unit. Use labeled nodes for maritime trade, colonial disruption, Cold War strategy, ASEAN institutionalization, and shared experience in diversity, with arrows converging on a central label 'Southeast Asia as political category'. Minimal cream background, navy lines, muted teal and gold accents, no flags, no cartoons, no small unreadable text.

2. Mandala
   - Asset path: `Study Guides/assets/midterm_theory_reference_v1.3.0/mandala_fading_authority_rings.png`
   - Graph logic: Radial diagram: sacred/commercial center, fading authority rings, conditional peripheral allegiance.
   - Prompt: Create a polished conceptual diagram of a precolonial Southeast Asian mandala polity. Show a bright central court or port hub, concentric rings of fading authority, tribute and trade arrows, and peripheral chiefs with conditional allegiance. Academic reference-sheet style, flat vector-like illustration, navy/teal/gold palette, labels limited to center, tribute, trade, fading authority, no modern borders, no cartoon people.

3. Sinic village governance
   - Asset path: `Study Guides/assets/midterm_theory_reference_v1.3.0/sinic_village_civic_capital_flow.png`
   - Graph logic: Causal flow: Dai Viet state delegation -> village councils/quotas/public works -> civic capital -> modern public goods/consumption.
   - Prompt: Create a horizontal causal-flow graphic for Dell, Lane, and Querubin's Vietnam village-governance argument. Show Dai Viet state delegation leading to village councils, tax and conscription quotas, public works, repeated cooperation, civic capital, and modern public goods and consumption. Clean graduate political-economy style, subtle map-boundary motif, navy text boxes, green arrows, no decorative characters, no tiny paragraphs.

4. Diamond geography
   - Asset path: `Study Guides/assets/midterm_theory_reference_v1.3.0/diamond_geography_scale_ladder.png`
   - Graph logic: Scale ladder: continental biogeography -> proximate conquest toolkit -> institutional mediation -> within-SEA variation.
   - Prompt: Create a conceptual scale-ladder diagram for Jared Diamond's geography argument as used in Southeast Asia politics. Show bottom layer 'continental biogeography', then domesticable species and east-west diffusion, then guns/germs/steel as proximate toolkit, then institutional mediation, ending with a warning label 'too coarse for within-SEA variation'. Editorial academic style, restrained colors, simple icons for crops, animals, ships, and institutions, no deterministic world map.

5. European diversion
   - Asset path: `Study Guides/assets/midterm_theory_reference_v1.3.0/european_diversion_timeline.png`
   - Graph logic: Timeline: Rome collapse -> feudalism -> free towns/merchant coalitions -> nation-states -> naval projection into SEA.
   - Prompt: Create a compact timeline graphic titled European Diversion for a politics study guide. Show five stages: Fall of Rome, feudal security bargains, free towns and merchant coalitions, fiscal-military nation-states, overseas naval projection into Southeast Asia. Use small symbolic icons, arrows, and one contrast callout 'mandalas stayed flexible/personalistic'. Navy, slate, and gold palette, clean print-friendly layout, no crowded text.

6. AJR reversal
   - Asset path: `Study Guides/assets/midterm_theory_reference_v1.3.0/ajr_reversal_extractive_spillover.png`
   - Graph logic: Mechanism map: VOC monopoly violence -> output restriction/autarky -> destroyed commerce -> reversal of development.
   - Prompt: Create an academic mechanism map for Acemoglu and Robinson's reversal-of-development argument in the Moluccas. Show VOC monopoly violence leading to spice-tree destruction, output restriction, defensive autarky by neighboring polities, destroyed commerce, and long-run underdevelopment. Use an abstract island-and-trade-network motif, red only for coercion, navy/gray for institutions, concise labels, no gore, no stereotyped imagery.

7. Dell-Olken Java
   - Asset path: `Study Guides/assets/midterm_theory_reference_v1.3.0/dell_olken_java_factory_catchment.png`
   - Graph logic: Spatial diagram: sugar factory catchment radius, roads/rail/irrigation/schools, durable agglomeration.
   - Prompt: Create a spatial political-economy diagram for Dell and Olken's Java Cultivation System findings. Show a sugar factory at center, a 4-7 km catchment ring, cane villages, roads, rail, irrigation, schools, and modern manufacturing clustering around the old factory site. Clean reference-sheet graphic, muted green and navy palette, precise labels, no romantic plantation imagery, no people in distress.

8. Stubbs war and EOI
   - Asset path: `Study Guides/assets/midterm_theory_reference_v1.3.0/stubbs_war_eoi_conditional_path.png`
   - Graph logic: Conditional path: war/security pressure + aid/market access + elite weakening -> strong state -> EOI, with Philippines failure branch.
   - Prompt: Create a conditional causal-path diagram for Richard Stubbs on war and export-oriented industrialization. Show war and Cold War security pressure, U.S./Japanese aid and market access, elite disruption, strong state formation, and EOI success. Include a clearly marked Philippines failure branch where landed elites and weak tax capacity survive. Academic flowchart style, navy boxes, teal success path, amber caution branch, no battlefield imagery.

9. Thailand miracle
   - Asset path: `Study Guides/assets/midterm_theory_reference_v1.3.0/thailand_non_developmental_state_growth_mix.png`
   - Graph logic: Balance chart: open economy, Chinese-Thai entrepreneurs, macro stability, land frontier, demography -> growth; 1997 fragility limit.
   - Prompt: Create a polished balance-chart graphic for Thailand's non-developmental-state miracle. Show growth inputs on one side: open economy, Chinese-Thai entrepreneurial class, macro stability, land frontier, demographic transition, and cautious pro-business state. Show 1997 crisis, financial fragility, and inequality as limit tests on the other side. Graduate study-guide style, Thai case without flags or tourist imagery, navy/green/gold palette.

10. Singapore model
   - Asset path: `Study Guides/assets/midterm_theory_reference_v1.3.0/singapore_state_capitalism_control_panel.png`
   - Graph logic: Control-panel diagram: PAP state coordinates labor, savings, land, infrastructure, MNE attraction, logistics.
   - Prompt: Create a clean control-panel style conceptual graphic for the Singapore development model. Center a capable PAP state coordinating labor discipline, CPF forced savings, land assembly, public housing, infrastructure, MNE-led manufacturing, and port/logistics services. Show markets operating inside state-shaped conditions, not laissez-faire. Modern editorial style, navy and teal with gold highlights, no skyline photo, no flag, no propaganda feel.

11. Hicken AFC paradox
   - Asset path: `Study Guides/assets/midterm_theory_reference_v1.3.0/hicken_crisis_reform_pressure_paradox.png`
   - Graph logic: Two-line comparison: Thailand severe shock -> reform pressure; Philippines mild shock -> institutional stickiness.
   - Prompt: Create a two-track comparison graphic for Allen Hicken's Asian Financial Crisis reform-pressure paradox. Top track: Thailand, severe 1997 shock, visible institutional failure, reform pressure. Bottom track: Philippines, milder shock, status quo coalition survives, weak institutions remain sticky. Use simple line graphs or pressure gauges, academic reference-sheet style, navy/amber/teal palette, no stock-market clutter, concise labels.

## Build / Verification

- Builder: `GPPS 463 - Pol SEA - Ravanilla/Study Guides/build_midterm_theory_reference.py`
- Output: `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.3.0.pdf`
- Tooling: ReportLab and pypdf.
- Verification performed:
  - Generated the PDF successfully.
  - Confirmed page count is 23: one cover page plus 11 two-page theory/framework spreads.
  - Confirmed PDF outline/bookmarks are present for all 11 framework pages.
  - Confirmed bookmark destinations map to pages 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, and 22.
  - Confirmed 11 clickable TOC link annotations on the cover page.
  - Confirmed no blank pages.
  - Confirmed text extraction returns 55,812 characters.
  - Confirmed extracted PDF text contains `CONCEPTUAL VISUAL SLOT`, `ELI5 CONCLUSION`, `Study Guides/assets/midterm_theory_reference_v1.3.0`, and `GPT-5 via Codex (reasoning effort not exposed)`.
  - Confirmed v1.2.0 PDF and notes remained present and were not modified by this pass.

## Sources Used

The v1.3.0 revision reused the v1.2.0 source base:

- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/Midterm_1_Study_Guide.md`
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/Midterm_1_Index_Cards.md`
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/Midterm_1_Lecture_Gaps.md`
- `GPPS 463 - Pol SEA - Ravanilla/W2 - Sinivs Indi, Guns Germs & Steel/Week 2 Reference Summary.pdf`
- `GPPS 463 - Pol SEA - Ravanilla/W3 - Colonial Institutions and Development/W3 Theory Reference.pdf`
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Week_4_Reference.pdf`
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/jansen2001_thailand_miracle_summary.md`
- `GPPS 463 - Pol SEA - Ravanilla/Study Guides/huff1995_singapore_model_summary.md`
- `GPPS 463 - Pol SEA - Ravanilla/W5 - Singapore & Asian Financial Crisis/Discussion Post LD10 - Asian Financial Crisis.md`
- `GPPS 463 - Pol SEA - Ravanilla/Course Admin/syllabus_extracted.md`
- `GPPS 463 - Pol SEA - Ravanilla/_agent/AGENT_CONTEXT.md` and `FEEDBACK.md`

## References

Acemoglu, D., & Robinson, J. A. (2012). Reversing development. In *Why nations fail: The origins of power, prosperity, and poverty*. Crown.

Dell, M., Lane, N., & Querubin, P. (2018). The historical state, local collective action, and economic development in Vietnam. *Econometrica*, *86*(6), 2083-2121. https://doi.org/10.3982/ECTA15122

Dell, M., & Olken, B. A. (2020). The development effects of the extractive colonial economy: The Dutch Cultivation System in Java. *Review of Economic Studies*, *87*(1), 164-203. https://doi.org/10.1093/restud/rdz017

Diamond, J. (1997). Prologue: Yali's question. In *Guns, germs, and steel: The fates of human societies*. W. W. Norton.

Hayton, B. (2014). Wrecks and wrongs: Prehistory to 1500. In *The South China Sea: The struggle for power in Asia*. Yale University Press.

Hicken, A. (2008). The political economy of the Asian financial crisis. Course reading PDF.

Huff, W. G. (1995). What is the Singapore model of economic development? *Cambridge Journal of Economics*, *19*(6), 735-759.

Jansen, K. (2001). Thailand: The making of a miracle? *Development and Change*, *32*(3), 343-370.

Stubbs, R. (1999). War and economic development: Export-oriented industrialization in East and Southeast Asia. *Comparative Politics*, *31*(3), 337-355. https://www.jstor.org/stable/422343

---
Generated for: Edgar Agunias
Date: 2026-04-30
Model: GPT-5 via Codex (reasoning effort not exposed)
Sources: Existing GPPS 463 study guides, Week 2/W3/W4 reference PDFs, syllabus extraction, Poseidon course memory, v1.2.0 builder and notes
Agent: Poseidon
---
