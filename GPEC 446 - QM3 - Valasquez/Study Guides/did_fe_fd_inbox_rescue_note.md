# DiD, Fixed Effects, and First Differences - Inbox Rescue Note

## Bottom Line

Yes: the two DiD/FE/FD inbox PDFs contain the missing panel-data material Tyche had been waiting on. They add the course-specific classroom version of:

- two-by-two Difference-in-Differences (DiD);
- how to interpret every coefficient in the canonical DiD regression;
- why two-period DiD, first differences, and fixed effects recover the same treatment effect in the simple setup;
- the business-training numerical example Edgar should be ready to compute by hand.

The third file, `week3_IV_exercise_v2.pdf`, is IV review, not missing DiD material. It belongs with the existing IV folder.

## Source Files Checked

- `inbox/QM3/Week 6 Exercises DiD FE FD.pdf`
- `inbox/QM3/Interpreting all β's in DiD.pdf`
- `inbox/QM3/week3_IV_exercise_v2.pdf`

All three were machine-readable with `pdftotext`; no OCR was needed.

## The Core DiD Example

The class example gives average daily sales:

| Group | Baseline | Endline | Change |
|---|---:|---:|---:|
| Treatment | 145 | 180 | 35 |
| Control | 165 | 170 | 5 |

The DiD estimate is:

```text
DiD = (Y_T,post - Y_T,pre) - (Y_C,post - Y_C,pre)
DiD = (180 - 145) - (170 - 165)
DiD = 35 - 5
DiD = 30
```

Plain-English interpretation: access to the training program is associated with a 30-dollar increase in average daily sales above and beyond the background change observed in the control group.

## Targeting and Bias

At baseline, treated firms have lower sales than control firms: 145 vs. 165. That means the intervention was negatively targeted on baseline sales volume, in the sense that lower-sales businesses were selected into treatment.

A naive post-treatment cross-sectional estimate would compare 180 vs. 170 and conclude a 10-dollar treatment-control gap. That is biased downward relative to the DiD estimate of 30 because it ignores the treated group's lower starting point.

The control group's role is to estimate the counterfactual time trend: how treated firms would likely have changed from baseline to endline if they had not received the training.

## Parallel Trends

One-sentence assumption:

> In the absence of treatment, treated and control firms would have followed the same outcome trend over time.

Parallel trends does not require treated and control groups to have the same baseline level. It requires their untreated changes over time to be comparable. In the example, treated firms can start 20 dollars below controls; the identifying claim is that the control group's +5 trend is the right counterfactual trend for treated firms without training.

## Canonical DiD Regression

The classroom regression is:

```text
Y_it = b0 + b1 Treat_i + b2 Post_t + b3 (Treat_i * Post_t) + e_it
```

Where:

- `Treat_i = 1` for treated units and `0` for controls.
- `Post_t = 1` in the post-treatment period and `0` in the pre-treatment period.
- `Treat_i * Post_t = 1` only for treated units after treatment.

Coefficient interpretations in the class example:

| Coefficient | Meaning | Example value |
|---|---|---:|
| `b0` | Control-group baseline mean | 165 |
| `b1` | Baseline treated-control difference | 145 - 165 = -20 |
| `b2` | Control-group time trend | 170 - 165 = 5 |
| `b3` | DiD treatment effect | 30 |

Predicted cell means:

```text
Control, pre:     b0
Treatment, pre:   b0 + b1
Control, post:    b0 + b2
Treatment, post:  b0 + b1 + b2 + b3
```

Exam move: if asked "what does each beta capture?", do not say all coefficients are treatment effects. Only `b3` is the DiD treatment effect. `b1` is a baseline group gap, and `b2` is the control trend.

## First Differences

With two periods, first differencing subtracts each unit's baseline outcome from its endline outcome:

```text
Delta Y_i = Y_i1 - Y_i0
Delta D_i = D_i1 - D_i0
```

In the firm-level table:

- treated firms have `Delta D = 1`;
- control firms have `Delta D = 0`;
- stable variables such as location and size have no change if measured as time-invariant traits.

The first-difference regression is:

```text
Delta Y_i = a + beta Delta D_i + Delta e_i
```

Because all stable unit-level traits disappear after differencing, the coefficient on `Delta D_i` is the treated group's average change minus the control group's average change. In this simple two-period case, that equals the hand-computed DiD.

Using the firm-level table, the treated changes are 35, 35, 37, and 33, with mean 35. The control changes are 5, 5, 7, and 3, with mean 5. So the first-difference coefficient is:

```text
35 - 5 = 30
```

## Fixed Effects

The fixed-effects version is:

```text
Y_it = alpha_i + lambda_t + beta D_it + e_it
```

In R, the classroom implementation is:

```r
lm(Y ~ D + factor(firm_id) + factor(t))
```

Interpretation:

- `alpha_i` absorbs firm fixed effects: all stable firm traits, such as baseline quality, management style, location if it does not change, and other time-invariant differences.
- `lambda_t` absorbs time fixed effects: shocks common to all firms in the post period.
- `D_it` turns on only for treated firms in the post period.
- `beta` is the within-firm treatment effect after removing stable firm differences and common time shocks.

In the two-group, two-period setup, `beta` equals the hand-computed DiD and the first-difference estimate: 30.

## Two Periods vs. More Periods

The exercise asks whether these estimates would be the same in three periods. The safe answer:

In exactly two periods with one treatment group and one control group, DiD, first differences, and fixed effects are algebraically equivalent ways to remove baseline group differences and common time shocks. With three or more periods, they need not line up mechanically because treatment timing, dynamic effects, pre-trends, and weighting across periods can matter. The interpretation moves from one clean before-after contrast to a panel design that must be checked for timing and trend assumptions.

## What Edgar Should Memorize

- DiD is a change-in-changes estimator, not a post-only group comparison.
- `b3` in `Y_it = b0 + b1 Treat_i + b2 Post_t + b3 Treat_i*Post_t + e_it` is the DiD effect.
- `b0` is control pre, `b1` is the baseline treated-control gap, `b2` is the control trend, and `b3` is the extra treated-group change.
- Parallel trends is about untreated trends, not equal levels.
- In the simple two-period case, DiD = first differences = fixed effects.
- FE removes time-invariant unit heterogeneity; it does not solve time-varying confounding.
- A pre-existing treated-control level gap is allowed; a pre-existing treated-control trend gap is dangerous.

## Sorting Recommendation

Do not move files without Edgar's permission. Recommended course-folder sorting:

- Move `inbox/QM3/Week 6 Exercises DiD FE FD.pdf` to a new topic folder such as `GPEC 446 - QM3 - Valasquez/W5 - Panel Data & DiD/`.
- Move `inbox/QM3/Interpreting all β's in DiD.pdf` to the same new `W5 - Panel Data & DiD/` folder.
- Move `inbox/QM3/week3_IV_exercise_v2.pdf` to `GPEC 446 - QM3 - Valasquez/W4 - Instrumental Variables/`, alongside the existing IV lecture/exercise material.

The DiD files should not be buried in `W4 - Instrumental Variables/`, because their topic is panel data, DiD, first differences, and fixed effects.

## References

Alulu, V. (2026, April 23). *Interpreting all beta's in DiD* [Course handout]. GPEC 446 Quantitative Methods III, UC San Diego.

Alulu, V. H. (2026, April 16). *Week 3 in-class exercise: Instrumental variables* [Course slides]. GPEC 446 Quantitative Methods III, UC San Diego.

McIntosh, C. (2026, April 23). *Week 6 exercises: DiD, FE, FD* [Course slides]. GPEC 446 Quantitative Methods III, UC San Diego.

---
Generated for: Edgar Agunias
Date: 2026-04-30
Model: GPT-5 Codex
Sources: Local QM3 inbox PDFs listed above; Tyche memory; existing QM3 syllabus extraction and study-guide folder context
Agent: Tyche
---
