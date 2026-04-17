# GPEC 446 — Week 4 Prep Brief

**Course:** GPEC 446 Quantitative Methods 3 (Valasquez)
**Week:** 4 — Panel Data Basics (Fixed Effects + DiD)
**Built:** 2026-04-16
**Agent:** Tyche

---

## TL;DR

- **Week 4 per the syllabus is Panel Data Basics** — fixed effects, DiD setup, parallel trends. This is genuinely new material not yet covered in any reference manual.
- **Week 4 slides have not been posted yet.** The only file currently in the `W4 - Instrumental Variables/` folder is `QM3_L5_IV.pdf`, which is IV material (the syllabus's Week 3 topic). No new Week 4 handout or slide deck has dropped.
- **This brief is the fallback.** It tells you where to self-study in the meantime, previews the Week 4 syllabus topics so you walk in oriented, and lists what to do the moment the real slides appear.
- A full `GPEC_446_Week_4_Reference.pdf` will be built once Valasquez posts the Week 4 slides and any handout.

---

## Important folder vs syllabus correction

The course folder has a naming drift worth noting.

| Source | Week 3 | Week 4 |
|---|---|---|
| Syllabus (`Course Admin/QM3_Syllabus.pdf`, p. 4) | Instrumental Variables | Panel Data Basics (FE, DiD) |
| Course folder (as laid out 2026-04-15) | `W3 - Regression/` | `W4 - Instrumental Variables/` |

The folder structure follows the **lecture-number sequence** (L1 Intro, L2 Causal, L3 Regression I, L4 Regression II, L5 IV), which puts IV in "W4" because it is the fifth lecture. The syllabus uses **week-of-instruction numbering**, which puts IV in Week 3 (since Weeks 1–2 each got one lecture while Week 3 picks up regression plus IV).

**What to do:** when Valasquez or the TA references "Week 4," assume syllabus numbering — panel data, not IV. If you want folder hygiene, consider renaming `W4 - Instrumental Variables/` → `W3b - Instrumental Variables/` or just `IV - Instrumental Variables/` once the Week 4 panel-data slides arrive and need their own folder. That is a housekeeping decision to make with Edgar; the brief doesn't touch the folder name unilaterally.

---

## Self-study pointer for the IV material you already have

L5 IV slides (`W4 - Instrumental Variables/QM3_L5_IV.pdf`) are **already fully synthesised** in the existing Lectures Manual v2.

Open `Study Guides/QM3_Lectures_Reference_Manual.pdf` and work through:

- **§2.4a Forward reference — ITT, LATE, compliers** (pp. 9–10). Bridges the ITT/take-up vocabulary the Week 1 exercises tested into the Wald-ratio preview.
- **§5 Instrumental Variables.** Full coverage: the three IV assumptions (relevance, exclusion, monotonicity), the Wald estimator, 2SLS mechanics, weak-instrument diagnostics (Stock-Yogo and the Lee et al. 2022 update), and bad-controls/post-treatment-bias logic.
- **Abbreviation decoder + cheat sheet** (pp. 28–30). Both contain ITT, LATE, Wald, exclusion, relevance, compliers, monotonicity as one-line refresh prompts.

If Valasquez opens Week 4 with a DiD/FE recap that references IV as a contrast case ("when you can find a valid instrument, do IV; when you can't but you have panel data, do DiD"), §5 of the Lectures Manual is enough context. You do not need a separate IV reference PDF.

**Pair this with:** *Mastering 'Metrics*, Ch. 3 (the full IV chapter — same material the Lectures Manual §5 abstracts). Good to skim if the professor starts cold-calling.

---

## What Week 4 will actually cover (syllabus preview)

From the syllabus (p. 4):

> **Week 4: Panel Data Basics**
> - Panel data structure
> - Fixed effects
> - Difference-in-differences (DiD) model
>
> Suggested reading: *Mastering 'Metrics*, Ch. 5; Wooldridge, Ch. 13.

### Expected concept load

The three bullets map to a tight cluster of methods. Based on the syllabus ordering (panel → FE → DiD) and the Mastering Metrics Ch. 5 table of contents, expect the lecture to move in this order:

1. **Panel data structure.** Stacked data indexed by unit `i` and time `t`. Key distinction from cross-section: you observe the same unit multiple times, so you can difference out unit-specific unobservables.
2. **Fixed effects (FE).** The workhorse trick: include a dummy for every unit (or every time period, or both). Formally absorbs all time-invariant unit heterogeneity. Mechanically equivalent to the within transformation `Y_it − Ȳ_i` or to running OLS with `factor(id)` in R.
3. **Two-way fixed effects (TWFE).** Unit FE *and* time FE. Absorbs time-invariant unit heterogeneity and unit-invariant time shocks simultaneously. The default starting specification for policy-evaluation panel data.
4. **DiD as a special case of TWFE.** Two groups (treated, control), two periods (pre, post). The DiD estimator is the coefficient on the `Treated × Post` interaction in a TWFE regression:

   ```
   Y_it = α_i + λ_t + β (Treat_i × Post_t) + ε_it
   ```

   β is the DiD estimate.
5. **Parallel trends.** The identifying assumption. Treated and control groups would have evolved in parallel absent the treatment. Tested visually (pre-period trend plot) and formally (placebo regression on pre-period years).
6. **Clustering.** Standard errors need to be clustered at the unit level because errors are serially correlated within a unit. `feols(... , cluster = ~id)` or `lm_robust(... , clusters = id)` in R.

Mastering Metrics Ch. 5 demonstrates all of this with the **Mississippi banking experiment** (Great Depression, Atlanta Fed's Sixth District liberal lending vs. St. Louis Fed's Eighth District tight policy). Read Ch. 5 §5.1 and §5.2 before class; it is the most didactic DiD walkthrough in the book.

### What you already know that transfers directly

From the Lectures Manual:

- **OVB logic (§4.3).** FE is the OVB solution when the omitted variable is time-invariant at the unit level. Same bias formula; FE just sets it to zero by construction for those confounders.
- **Cov/Var OVB notation (§4.3 callout).** Valasquez's exercise-style notation will carry straight into panel data — expect c1 = Cov(Y, W)/Var(W) and c2 = Cov(W, X)/Var(X) to reappear with W as a time-invariant unobservable.
- **CIA (§3.4 / §4.1).** Parallel trends is the DiD analogue of CIA. Instead of conditioning on observables, you condition on unit-level fixed effects and a common time shock. The defense is the same species of argument ("what story about unobservables would break this?") just applied to a different selection problem.
- **IV as a contrast (§5).** When a credible instrument exists, IV handles any source of endogeneity including time-varying confounders. FE handles only time-invariant confounders but does not need an instrument. DiD sits between: handles time-invariant unit effects and common time shocks but assumes parallel trends.

### R tooling you already have from the Labs Manual

- `feols(Y ~ X | fe1 + fe2, data = df, cluster = ~id)` — from the Labs Manual §R reference. This is the one-liner for TWFE with clustered SEs.
- `lm(Y ~ X + factor(id) + factor(year), data = df)` — slower but transparent equivalent. Useful when you want to see every fixed-effect coefficient.
- `plm::plm()` — the canonical panel-data package. Edgar has not used it in lab yet; the Wooldridge Ch. 13 reading may introduce it.

---

## What this brief deliberately does NOT contain

- **No new formulas derived.** The DiD estimator, TWFE matrix algebra, and parallel-trends test statistics will come from the Week 4 slides. Building them from textbook now risks notation drift from what Valasquez actually teaches.
- **No worked numerical example.** Mastering Metrics Ch. 5 has the Mississippi example; read it there so you see Angrist and Pischke's prose alongside the numbers.
- **No cheat-sheet row or decoder update.** Those go into the Lectures Manual v3 once Week 4 content solidifies.

---

## Action items once Week 4 slides drop

1. **Inventory the new material.** Run the `lecture-to-reference-pdf` skill's Step 0 content inventory on the Week 4 slide deck and any handout. List every formula, every term, every worked example.
2. **Decide: addendum or v3 rebuild?**
   - If Week 4 adds ≤4 pages of content and has no notational conflicts with v2: build `GPEC_446_Week_4_Reference.pdf` as a standalone addendum in `Study Guides/`, cross-referencing Lectures Manual §2.4a / §5.
   - If Week 4 introduces cross-cutting notation (e.g., a different OVB rewrite, new "W" variable convention): preserve v2 as `_v2.pdf` and build `QM3_Lectures_Reference_Manual.pdf` v3 with panel-data sections 6–8 added.
3. **Update the Lectures Manual v2 assumptions summary.** Add parallel trends, no anticipation effects, SUTVA-in-panel, and clustering conventions.
4. **Update the decoder.** Add TWFE, FE, DiD (already there), parallel trends, placebo test, clustering, within estimator.
5. **Add R snippets.** `feols()` with two-way FE, `plm::plm()` equivalent, parallel-trends pre-period plot with `ggplot2 + geom_line`, placebo regression for lead terms.
6. **Cross-check against the Labs Manual.** If Lab 3 or Lab 4 drops for Week 4, those need the same integration treatment into `QM3_Labs_Reference_Manual.pdf`.

---

## Pre-class reading checklist (do before Week 4 meets)

- [ ] *Mastering 'Metrics* Ch. 5 §5.1 (Mississippi experiment setup) — p. 175 or thereabouts in the course-folder PDF
- [ ] *Mastering 'Metrics* Ch. 5 §5.2 (regression DD and parallel trends)
- [ ] Lectures Manual v2 §2.4a + §5 (IV refresher; makes the FE-vs-IV contrast land)
- [ ] Labs Manual §R reference: re-read the `feols()` syntax row, including the `| fe1 + fe2 |` and `cluster = ~id` pieces
- [ ] Optional: Wooldridge Ch. 13 — denser than Angrist/Pischke but the canonical graduate treatment of panel data. Skim the first 10 pages for the within-estimator derivation

---

## One-paragraph elevator pitch for DiD

If someone asks you to explain DiD cold, say this:

> "DiD is a causal-inference design for settings where a policy is rolled out to one group at a specific moment in time and not to another group. You observe both groups before and after. The core insight is that if the two groups were on parallel paths before the policy, their paths would have stayed parallel in the absence of the policy — so any divergence after the policy is the causal effect. The estimator is the change in the treated group's outcome minus the change in the control group's outcome, which in regression form is the coefficient on the interaction of a Treated dummy with a Post dummy, fit with unit and time fixed effects."

This is the elevator pitch Valasquez's cohort-style exercises will drill. Keep it handy.

---

## Source notes

- Syllabus page references: `Course Admin/QM3_Syllabus.pdf`, Course Outline pp. 4–5 (Weeks 1–5 laid out).
- Textbook: Angrist and Pischke, *Mastering 'Metrics* (2014, Princeton UP), Ch. 5 §5.1 opens at the "Mississippi Experiment" header.
- Existing synthesis: `Study Guides/QM3_Lectures_Reference_Manual.pdf` v2 (32 pp., built 2026-04-16), §2.4a + §5 + cheat sheet + decoder.
- No Week 4 source material exists in the workspace as of 2026-04-16.

---

### Output Disclosure

- **Model:** claude-opus-4-7[1m]
- **Date:** 2026-04-16
- **Agent:** Tyche (GPEC 446 class agent)
- **Generated for:** Edgar Agunias
- **Sources:** `Course Admin/QM3_Syllabus.pdf` (Week 4 topic confirmation), `Study Guides/QM3_Lectures_Reference_Manual.pdf` v2 (IV coverage cross-check), `W4 - Instrumental Variables/QM3_L5_IV.pdf` (Week 4 folder inventory), `Joshua D. Angrist, Jörn-Steffen Pischke - Mastering 'Metrics` (Ch. 5 opening, p. ~175), workspace file inventory dated 2026-04-16.
- **Notes:** Fallback brief produced in lieu of a full `GPEC_446_Week_4_Reference.pdf` because no Week 4 slides or handouts have been posted yet. Full reference PDF to be built once source material is in hand.
