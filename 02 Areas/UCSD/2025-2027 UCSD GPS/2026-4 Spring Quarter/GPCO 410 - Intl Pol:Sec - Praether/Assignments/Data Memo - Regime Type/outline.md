# Data Memo — Outline

**Deliverable:** 3-page data memo on Polity IV/V regime-type coding, using Myanmar as the anchor case. Due May 15 at 5:00pm (pending deadline confirmation — see `prompt.md` TODO).
**Status:** First-draft outline. No prose yet. Do not draft paragraphs against this file until Edgar signs off on the central question and the pivot choice.

## Central question (placeholder — pick one before drafting)

**Option A (recommended):** How does Polity V code Myanmar's 2010–2018 partial democratization, why does that coding inflate Myanmar's `polity2` score relative to a structural reading of the 2008 constitution, and what does the gap tell us about quantitative findings that democratization raises civil war risk?

**Option B:** How should Polity code the 2021 Myanmar coup given that Polity V v2018 ends at 2018, and what do the codebook's special-code rules imply about the correct coding?

**Option C:** Why does Polity's observed-behavior coding philosophy produce different results for guardianship regimes (Myanmar, Thailand, Turkey pre-2001) than a structural-constraint coding would, using Myanmar 2015–2020 as the anchor case?

Athena recommends **Option A** — it is in-sample for Polity5 v2018, it avoids pivoting on a gap in the data, and it yields a clean "here's the coding, here's how I'd recode it, here's what that breaks for published findings" arc that Prather's rubric rewards.

## Structure — 6 body beats mapping to the rubric

The syllabus rubric (9 questions) maps cleanly to 6 beats. Each beat handles 1–2 rubric questions.

### Beat 1 — Research question and dataset (~150 words)

Rubric questions answered: #1 (dataset), #2 (observation), #3 (aspect).

- Name the question (Option A as drafted above).
- Name the dataset: Polity V (Polity5), Center for Systemic Peace, Annual Time-Series 1946–2018. Cite codebook and INSCR download page in first footnote.
- Name the observation: Myanmar (ccode 775), years 2010–2018.
- Name the aspect: `polity` / `polity2` score during the partial democratization, with specific attention to `xconst` (executive constraints) and `parcomp` (competitiveness of political participation).

### Beat 2 — How Polity codes this observation (~200 words)

Rubric questions answered: #4 (how coded).

- Report Myanmar's actual Polity values 2010–2018 (`polity`, `polity2`, `xconst`, `parcomp`, `durable`) in a small inline table or a sentence. Edgar to pull from downloaded `p5v2018.xls`.
- Contrast the 2010 election coding (USDP win under 2008 constitution, NLD boycotting) with the 2015 election coding (NLD landslide, civilian government takes office).
- Note the `polity2` interpolation rule: transition years (−88) get prorated linearly; foreign-interruption years (−66) stay missing; interregnum years (−77) get set to 0.

**Evidence peg:** actual `polity2` trajectory: −8 through 2009 → rises through the 2010–2015 window → settles at +8 from 2016 onward (pending verification at data acquisition).

### Beat 3 — Why Polity codes it that way (~200 words)

Rubric questions answered: #5 (why coded that way).

- Polity's conceptual framework treats democracy as a set of **institutional rules and observed political behaviors** — openness of executive recruitment, competitiveness of participation, constraints on executive. Codebook §3.
- `xconst` is scored from observed behavior of the executive: does the executive face institutional constraints on decision-making? After 2015, the NLD-led executive was constrained by the Tatmadaw's constitutional reservations — Polity coded this as "substantial" or higher executive constraints.
- The coding is internally consistent with Polity's philosophy. The issue the memo will raise is that the philosophy itself under-weights reserved-domain autocracy — where the constitutional structure preserves a non-electoral veto — because it treats observable electoral competition as the primary signal.
- Cite Marshall & Gurr codebook §3 and §4 with specific section numbers in footnotes.

### Beat 4 — Coding critique (~250 words)

Rubric questions answered: #6 (is the coding problematic?), #7 (alternative coding).

- **Yes, the coding is problematic.** Myanmar 2016–2020: 25% of parliament reserved for the Tatmadaw (Article 109/141), all security ministries under military control (Article 232), constitutional amendment requires >75% of parliament (Article 436). The NLD-led government could not direct the armed forces, could not appoint the security cabinet, and could not pass constitutional amendments. A Polity2 score of +8 treats this as comparable to post-authoritarian transitions that have eliminated reserved military domains (e.g., Argentina post-1983, Spain post-1981).
- **Alternative coding:** lower `xconst` to reflect the reserved domain. On Polity's 1–7 `xconst` scale, a reading treating the Tatmadaw's reserved seats and constitutional veto as a "significant limitation" would score `xconst` at 3–5 rather than 6–7. That alone pulls `polity2` from +8 down to ~+3 to +4 for 2016–2020.
- **Concrete example to cite in the memo:** compare Myanmar 2016 (Polity2 = +8) to Thailand 2003 (Polity2 = +9 per Polity5 before the 2006 coup) — both regimes had a constitutionally entrenched military veto. Both were scored as high democracies by Polity despite structural guardianship features. Both saw subsequent coups.
- Engage Meng & Little 2024's objectivity test: Polity's coding is more objective than V-Dem's (based on observable institutional rules, not expert judgments of "free and fair"), so the critique here is not coder bias — it is conceptual weighting. This distinction is important and sharpens the argument.

### Beat 5 — Implications for IR (~200 words)

Rubric questions answered: #8 (give example), #9 (implications for understanding international politics).

- Cederman, Hug & Krebs 2010's finding that democratization raises civil war risk is built on Polity IV's period coding. If Myanmar 2010–2015 is not coded as a democratization period (because reserved-domain autocracy keeps the `polity2` score lower and the transition-period detection doesn't trigger), the sample of "democratizations" shrinks. Some of the finding's empirical weight may rest on reserved-domain cases that are not substantively democratizing.
- Generalizable claim: the democratization-violence literature may be picking up an artifact of Polity's observed-behavior coding philosophy. Guardianship regimes that Polity scores as "democratizing" are actually preserving a military veto, which is itself the instability-generating feature.
- Policy implication: democracy-promotion evaluations that rely on Polity score increases as a success metric may be rewarding reserved-domain autocracies. A better metric would weight structural constraints (military subordination to civilian authority, independent judiciary, constitutional protection against unilateral executive action).
- Final sentence pointing forward: the 2021 coup in Myanmar was the failure mode the coding mis-diagnosed.

### Beat 6 — Conclusion (~100 words)

- Restate the finding: Polity V codes Myanmar 2016–2020 as a +8 democracy in a way that misweights the 2008 constitution's reserved military powers.
- Restate the recommended fix: structural-constraint adjustment to `xconst`.
- Restate the downstream implication: quantitative work on democratization and civil war may be partially picking up reserved-domain autocracies, not democracies.
- Close on the theoretical link to the Myanmar analytic memo (Orange), without duplicating its argument.

## Word budget

- Beat 1 (question, dataset): 150
- Beat 2 (how coded): 200
- Beat 3 (why coded that way): 200
- Beat 4 (critique + alternative): 250
- Beat 5 (implications): 200
- Beat 6 (conclusion): 100
- **Total target: 1,100** — will need trimming to reach 950-word ceiling. Pressure-test each beat in first draft.

## Evidence / footnote plan

1. Polity V codebook §3, §4, §5, §6 — multiple footnotes.
2. Polity5 dataset access — one footnote to INSCR URL and access date.
3. 2008 Constitution of Myanmar Articles 109, 141, 232, 436 — one footnote.
4. Cederman, Hug & Krebs 2010 — one footnote for the democratization-civil-war finding that depends on Polity coding.
5. Meng & Little 2024 — one footnote to situate the measurement-critique literature.
6. V-Dem Polyarchy Index for Myanmar — optional, for comparison footnote.
7. Thailand comparator case — one footnote sourced to the Polity5 codebook country narrative and one secondary historical source.

## What this memo does NOT do

- Does NOT argue Myanmar was or was not democratic. It argues about how Polity codes partial democratizations with reserved military domains.
- Does NOT argue all quantitative IR is wrong. It argues one specific coding choice has downstream consequences for one specific published finding.
- Does NOT duplicate the Orange memo's argument about civil war risk. The two memos share a case but address different questions (analytic vs measurement).
- Does NOT engage V-Dem at length. Polity is the assigned dataset.

## Pre-flight screens

- [ ] Does the draft interrogate a *specific* coding rule (not the dataset as a whole)? Data memos that critique datasets in general score worse than ones that deconstruct one rule.
- [ ] Does the draft tell the reader exactly how the alternative coding would change the score, in concrete numbers?
- [ ] Does the draft connect the coding critique to a published finding that depends on the coding?
- [ ] Footnotes only. No in-text parentheticals.
- [ ] Under 3 pages, under 950 words for graded portion.
- [ ] AI-use disclosure attached per SOP.

## Open decisions for Edgar

1. **Option A vs B vs C** for the central question — Athena recommends A (in-sample, cleaner). Edgar to confirm.
2. **Depth on Cederman et al.** — one sentence, one paragraph, or one whole beat? Athena recommends one paragraph (inside Beat 5) to avoid duplicating Orange memo content.
3. **Thailand comparator** — include or drop? Including it strengthens the "guardianship regime" generalization but costs ~100 words. Athena recommends including it as one sentence in Beat 4 and one footnote, not a full paragraph.
4. **Structural `xconst` rescore number** — the memo should name a specific alternative score (3, 4, or 5). Edgar to decide based on reading the codebook §4 `xconst` coding rules.

---

Generated for: Edgar Agunias
Date: 2026-04-16
Model: Claude Opus 4.7 (1M context)
Sources: Polity V codebook structure (Marshall & Gurr), Meng & Little (PS 2024), Cederman Hug & Krebs (JPR 2010) — full reading notes at `Assignments/Orange Memo - Myanmar/reading_notes.md`, 2008 Constitution of Myanmar (Edgar to verify article numbers), `Study Guides/pre_midterm_strategy.md`, `data_plan.md` in this folder
Agent: Athena
