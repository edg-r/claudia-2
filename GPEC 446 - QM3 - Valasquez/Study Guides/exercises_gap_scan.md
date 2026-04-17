# QM3 Week 1 and Week 2 Exercises — Gap Scan Against Study Guides

Scan of the two in-class exercise handouts against the existing `QM3_Lectures_Reference_Manual.pdf` (26 pp.) and `QM3_Labs_Reference_Manual.pdf` (33 pp.), both generated 2026-04-15. Goal: can a student solve every exercise using only the two study guides, without going back to the raw slides or Angrist & Pischke?

**Sources scanned**
- `W1 - Intro & Randomisation/Week_1_Exercises.pptx` — 8 slides: Bono Familias CCT, four numbered exercises plus two AI-prompting examples
- `W2 - Causal Inference/Week_2_Exercises_final.pdf` — 7 pages: OVB (schooling/earnings), simultaneity (welfare/poverty), plus a "Further Practice" police/crime OVB walk-through
- `Study Guides/QM3_Lectures_Reference_Manual.pdf` (Lectures L1-L5)
- `Study Guides/QM3_Labs_Reference_Manual.pdf` (Labs 1-2)

**Solution key status**
- Week 1 pptx: handout only. No answer key. Exercise 5's "Optimal Prompt" text implicitly encodes the instructor's expected approach for Exercises 1c and 2b, but no numerical answers.
- Week 2 pdf: handout only. The police/crime "Further Practice" section walks through the OVB recovery mechanically (c1 ≈ 0.81, c2 ≈ 0.95, bias ≈ 0.77, estimated = 0.33, recover true) but stops before giving the final numerical answer ("Recover the true Effect. What do you observe?"). Edgar should compute 0.33 − 0.77 = −0.44 and verify that sign against his own work.

Neither file contains a complete solution key. Edgar should write out his own answers and verify with the TA.

---

## Gaps Found

### Gap 1 — Bias recovery formula "True = Estimated − Bias" [Lectures Manual] — MODERATE

**Where in the exercises:** Week 2, "Further Practice: Endogeneity via OVB" (police/crime). The handout states "True Effect = Estimated Effect − Bias" as a recall prompt and then asks the student to recover the true police coefficient.

**Where the gap is:** Section 4.3 (OVB) of the Lectures Manual defines `OVB = β̂_s − β̂_l = π1 × γ`, which is the right relationship, but the manual presents it as a decomposition of the short and long regression coefficients. It never rearranges the equation into the student-facing form `β_true = β_estimated − bias` that the exercise uses.

**Severity:** Moderate. The student can re-derive the rearrangement in one line, but the exercise asks for it directly and a student skimming the manual for the exact phrasing will not find it.

**Recommended fix:** Add one line to the Lectures Manual Section 4.3 callout box (or to the cheat sheet in Section 6) stating:

> `β_true = β_estimated − OVB`. Rearrangement of `β̂_s = β̂_l + OVB`. Use when you know the bias and want to recover the true coefficient (Week 2 police/crime exercise).

**Insertion point:** Lectures Manual p. 15 (Section 4.3, after the 2×2 sign table) or p. 21 (Cheat Sheet, OVB row).

---

### Gap 2 — OVB formula expressed as Cov/Var [Lectures Manual] — MODERATE

**Where in the exercises:** Week 2 police/crime "Further Practice" writes:
> c1 = Cov(Y, W) / Var(W) → effect of crime risk on crimes ≈ +0.81
> c2 = Cov(W, X) / Var(X) → effect of police on crime risk ≈ +0.95
> Bias = c1 × c2

**Where the gap is:** The Lectures Manual writes OVB as `π1 × γ`, where `π1` is defined verbally as "the slope from regressing the omitted variable on the treatment." The Cov/Var form is used separately in Section 3.1 for the simple OLS slope (`β̂1 = Cov(x,y) / Var(x)`). The manual does not connect the two notations, so a student reading the exercise has to recognise that `c1 = γ` and `c2 = π1` are the same objects written in Cov/Var form.

**Severity:** Moderate. The student can connect the dots, but the professor has clearly chosen to use Cov/Var notation for this exercise and the study guide uses π1/γ notation exclusively.

**Recommended fix:** In Lectures Manual Section 4.3 (p. 15), add a one-line equivalence note:
> Equivalently: `π1 = Cov(A, D) / Var(D)` (auxiliary regression of A on D) and `γ = Cov(Y, A) / Var(A)` (effect of A on Y). Bias = `π1 × γ` either way.

**Insertion point:** Right after the OVB formula box on Lectures Manual p. 15.

---

### Gap 3 — Numerical OVB worked example (Bono Familias / schooling-earnings style) [Lectures Manual] — MODERATE

**Where in the exercises:** Week 2 Q4 asks the student to compute the implied OVB when adding parents' education drops β̂₁ from 0.08 to 0.05, and to check it against the Q2 sign prediction. This is exactly the numerical computation the manual never walks through.

**Where the gap is:** Lectures Manual Section 4.3 walks through OVB conceptually with the private-school example (β̂_s = $20,000, β̂_l = $10,000, OVB = $10,000) but does not show the "decompose into π1 × γ" verification that the Labs Manual does perform on the CASchools data. The student who wants a template for Q4 has to jump to the Labs Manual to find it.

**Severity:** Moderate. The template exists but is in the Labs Manual under `pi_1 <- coef(aux_reg)['str']` / `gamma_hat <- coef(reg_long)['meal_pct']`. The Lectures Manual should cross-reference it or carry a mini version.

**Recommended fix:** In Lectures Manual Section 4.3, add a "Numerical verification" sub-callout:
> To verify OVB from two regressions: (i) run the short regression, get β̂_s; (ii) run the long regression, get β̂_l and γ̂; (iii) run the auxiliary regression of the omitted variable on the treatment to get π̂1; (iv) check β̂_s − β̂_l ≈ π̂1 × γ̂. See Labs Manual §2D (CASchools example) for R code.

**Insertion point:** Lectures Manual p. 14-15.

---

### Gap 4 — ITT and effect on takers / compliers [Lectures Manual] — CRITICAL

**Where in the exercises:** Week 1 Exercise 3d asks directly:
> A critic says: 'Only 65% of eligible households took up the program, so the study is invalid.' Is this correct? What effect does the 11 pp estimate capture, and what additional assumption would you need to recover the effect on takers?

This is an ITT-vs-TOT question. The exercise assumes the student can articulate that the 11 pp is the Intent-to-Treat (ITT) effect at the municipality level and that recovering the effect on takers requires an IV/LATE framework with an exclusion restriction.

**Where the gap is:** The Lectures Manual has ITT only as a forward-reference in the abbreviation decoder (p. 23): "Effect of being assigned to treatment, regardless of whether the unit actually took it. Covered Week 9 (non-compliance)." LATE is similarly listed as forward-only ("Introduced more formally in Week 3"). Neither is derived or shown in a formula.

**Severity:** Critical. A Week 1 exercise is explicitly testing ITT vocabulary and the ITT-vs-ATT-on-takers distinction, but the study guide punts both concepts to Weeks 3 and 9. A student relying only on the study guides cannot answer Q3d.

**Recommended fix:** Either
- (a) Add a short "Partial take-up and ITT" call-out to Lectures Manual Section 2.4 (Random Assignment), stating the ITT definition formally: `ITT = E[Y | assigned to treatment] − E[Y | assigned to control]`, and noting that under partial take-up ITT ≠ ATT unless take-up is 100% or effects are homogeneous; or
- (b) A half-page "Forward Reference: ITT, LATE, Compliers" appendix between Section 2 and Section 3 that states ITT, ATT-on-takers, LATE, and the Wald-ratio connection (IV on an assignment dummy = ITT ÷ take-up rate under exclusion). This is the cleanest because it also primes Lecture 5.

**Insertion point:** Lectures Manual p. 8-9 (Section 2.4 callout) is the minimum fix. The fuller forward-reference box at p. 9 is better.

---

### Gap 5 — Simultaneity bias: sign-of-bias shortcut [Lectures Manual] — MINOR

**Where in the exercises:** Week 2 Simultaneity Q3 asks "What can you say about the direction of the resulting simultaneity bias in the direct effect of the program on poverty?" The exercise expects the student to reason about the sign of α2 / (1 − α1α2) without needing to recompute the whole derivation.

**Where the gap is:** Lectures Manual Section 4.4 gives the full derivation and states the bias sign is `sign[α2 / (1 − α1α2)]`. Fine, but for a quick "what's the sign?" exercise the study guide buries the answer inside a multi-line derivation. A quick-reference sign table (like the OVB 2×2) would help.

**Severity:** Minor. Student can work it out.

**Recommended fix:** Add a one-row sign table to Section 4.4 similar to the OVB 2×2:

> | α1 (direct effect) | α2 (reverse) | 1 − α1α2 | Sign of bias |
> |---|---|---|---|
> | < 0 (program reduces outcome) | > 0 (outcome raises treatment) | ≈ 1 | > 0 — OLS overstates (bias toward zero or positive sign) |
> | < 0 | < 0 | ≈ 1 | < 0 — OLS understates |

**Insertion point:** Lectures Manual p. 15, end of Section 4.4.

---

### Gap 6 — Khuzdar/Maria selection-bias sign comparison framing [Lectures Manual] — MINOR

**Where in the exercises:** Week 1 Exercise 2c and Exercise 5 (Example 2) both ask Edgar to compare the direction of selection bias in the Bono Familias case to the Khuzdar/Maria insurance example from Angrist & Pischke Ch. 1. The instructor's "Optimal Prompt" even scaffolds this comparison.

**Where the gap is:** The Lectures Manual covers Khuzdar/Maria in Section 2.3 (p. 8) with the numerical table and the "-2 gap in Y(0)" point. Adequate. What is missing is an explicit "which way does the bias run" comparison note that connects: Khuzdar (low Y0) self-selects INTO treatment → E[Y(0)|D=1] < E[Y(0)|D=0] → selection bias negative → naive estimator understates; vs Bono Familias (high-readiness municipalities, high Y0) selected INTO treatment → E[Y(0)|D=1] > E[Y(0)|D=0] → selection bias positive → naive estimator overstates.

**Severity:** Minor. The student can derive this. But the exercise is explicitly asking for the comparison, and a one-line note in the manual would make the study guide directly usable.

**Recommended fix:** Append a final paragraph to Section 2.3 (Lectures Manual p. 8):
> Sign of selection bias depends on whose Y(0) is higher. When the treated group has lower Y(0) (Khuzdar — sickest select into insurance), selection bias is negative and the naive estimator understates the true effect. When the treated group has higher Y(0) (Bono Familias — highest-capacity municipalities selected first), selection bias is positive and the naive estimator overstates. Always identify "who is treated and what are their counterfactual outcomes" before signing the bias.

**Insertion point:** Lectures Manual p. 8, end of Section 2.3.

---

### Gap 7 — R helper for computing naive estimator / ATE from a potential-outcomes table [Labs Manual] — MINOR

**Where in the exercises:** Week 1 Exercise 1c asks the student to compute the naive estimator from the 4-row table. The "Optimal Prompt" in Exercise 5 rehearses exactly this: τN = Ȳ(1) − Ȳ(0) = (84+79)/2 − (68+73)/2 = 81.5 − 70.5 = 11 pp.

**Where the gap is:** The Labs Manual spends its R pages on STAR and CASchools (real datasets) and does not show a quick R snippet for computing τN from a small hand-built tibble — useful when Edgar wants to verify a pen-and-paper answer in R.

**Severity:** Minor. One-liner: `mean(y[d==1]) - mean(y[d==0])`.

**Recommended fix:** In Labs Manual Section 4A (copy-paste R Snippets), add a short "Toy example: naive estimator from a small table" block:

```r
toy <- tibble(unit = c('Norte','Sur','Este','Oeste'),
              d = c(1,1,0,0), y = c(84,79,68,73))
tau_N <- mean(toy$y[toy$d==1]) - mean(toy$y[toy$d==0])
tau_N   # 11
```

**Insertion point:** Labs Manual p. 29 (top of Section 4A) or add as an appendix to Section 1.

---

### Gap 8 — "Percentage points" vs "percent" convention [Both] — MINOR

**Where in the exercises:** Week 1 exercise is in percentage points (82% vs 71% enrollment → 11 pp). Week 2 exercise is in log-percent (β̂₁ = 0.08 → 8% increase in earnings). The Exercise 5 "Optimal Prompt" explicitly asks Edgar to express results in percentage points and flags that units matter.

**Where the gap is:** Neither manual has a short note on when to write "pp" vs "%". The lectures manual writes "8 to 13.5 percent (log points)" once for Dale & Krueger but does not explain the distinction.

**Severity:** Minor. Good hygiene for a memo, not exam-critical.

**Recommended fix:** Add a one-line glossary row to the abbreviation decoder (Lectures Manual p. 22-23) or a sidebar in Section 3.2:
> pp (percentage points) — additive difference between two percentages (71% → 82% = 11 pp, NOT 15.5%). Use when the outcome is already a rate. Use "%" or "log points" when the outcome is in levels and you are reporting elasticities (log(earnings) coefficient).

**Insertion point:** Lectures Manual abbreviation decoder (p. 22-23).

---

## Vocabulary Audit

Words or phrases used in the exercises that I checked against the decoder:

| Term | In decoder? | Where it appears |
|---|---|---|
| ATE, ATT, naive estimator, selection bias, τN, τi, Yi(1), Yi(0), Di | Yes | W1 throughout |
| CCT (conditional cash transfer) | No | W1 slides 2-8. Program-specific, low priority |
| OVB | Yes | W2 throughout |
| π1, γ, long/short regression | Yes (Section 4.3) | W2 Q1 |
| Simultaneity, reverse causality | Yes (Section 4.4) | W2 Simultaneity Q1-Q4 |
| Endogeneity, exogenous, endogenous regressor | Partial — used in context but not in decoder | W2 Police/Crime |
| ITT | Forward-reference only | W1 Q3d (CRITICAL, see Gap 4) |
| LATE, compliers, take-up | Forward-reference only | W1 Q3d (CRITICAL, see Gap 4) |

**Recommended additions to the decoder:** CCT (one line, defined in W1 slide 2); "endogenous / exogenous" (promote from implicit to a proper row). Both are minor.

---

## Summary and Recommendation

**Severity distribution**
- Critical: 1 gap (ITT / effect on takers in W1 Q3d — the study guide explicitly defers it but a Week 1 exercise tests it)
- Moderate: 3 gaps (bias rearrangement, Cov/Var form of OVB, numerical OVB worked example)
- Minor: 4 gaps (simultaneity sign shortcut, Khuzdar/Maria sign comparison note, R snippet for toy naive estimator, pp-vs-% convention)

**Rebuild needed?**
No. The two manuals cover the conceptual and computational backbone of both exercise sets. The Critical gap is a single pedagogical decision (defer ITT/LATE to Week 9) that the exercise handout violates. The three Moderate gaps are all in Section 4.3 of the Lectures Manual and could be handled with one extra page. A short **ADDENDUM** (2-3 pages) is the right move, not a full rebuild.

**Proposed addendum structure** (`Study Guides/QM3_Exercises_Addendum.pdf`, if requested):
1. Quick reference — rearranged OVB formulas (`β_true = β_estimated − bias`, `bias = π1 × γ = [Cov(A,D)/Var(D)] × [Cov(Y,A)/Var(A)]`)
2. Partial take-up and ITT (the Critical gap) — one page covering ITT definition, why ITT ≠ ATT under partial take-up, the Wald ratio preview
3. Sign-of-bias cheat sheets — OVB 2×2 (already in manual) plus the simultaneity sign table
4. R toy-example snippets — naive estimator from a 4-row tibble, OVB verification in 5 lines
5. Khuzdar/Maria vs Bono Familias selection-bias direction comparison

All other gaps are cosmetic and can be edited into the next rev of the Lectures Manual when the L6-L10 material arrives.

---

**Exercises-to-study-guide map for Edgar's revision**

| Exercise | Primary study-guide section | Gap flag |
|---|---|---|
| W1 Ex1 (potential outcomes) | Lectures §1.3-1.5 | none |
| W1 Ex2 (selection bias, ATT decomposition) | Lectures §2.3 | Gap 6 (minor) |
| W1 Ex3a-c (randomisation, ATE) | Lectures §2.4 | none |
| W1 Ex3d (take-up, effect on takers) | Lectures forward-ref only | **Gap 4 (critical)** |
| W1 Ex4 (bias direction scenarios) | Lectures §2.3 + §4.3 | none |
| W1 Ex5 (AI prompting) | N/A (meta) | none |
| W2 OVB Q1-Q3 (long/short, sign) | Lectures §4.3 | none |
| W2 OVB Q4 (numerical OVB from 0.08→0.05) | Lectures §4.3 + Labs §2D | Gap 3 (moderate) |
| W2 OVB Q5 (reliability without data) | Lectures §4.3 sign table | none |
| W2 Simultaneity Q1-Q4 | Lectures §4.4 | Gap 5 (minor) |
| W2 Further Practice (police/crime OVB recovery) | Lectures §4.3 | **Gap 1, Gap 2 (moderate)** |

---

Generated for: Edgar Agunias
Date: 2026-04-16
Model: Claude Opus 4.6 (1M context)
Sources: Week_1_Exercises.pptx (W1 folder), Week_2_Exercises_final.pdf (W2 folder), QM3_Lectures_Reference_Manual.pdf, QM3_Labs_Reference_Manual.pdf
Agent: Tyche (GPEC 446 class agent)
