# Homework 2 Report Skeleton

Edgar Agunias  
GPEC 446 - Quantitative Methods 3  
May 2026

## Part I: Panel and Two-Way Fixed Effects

### Question 1

**Prompt:** Generate a numeric country identifier and year dummies. Estimate pooled OLS and within regression for the relationship between governance (RHS) and income (LHS), controlling for year dummies where possible. Present results in a single table.

**Expected artifact:** `[table_q1_panel_models]`

**Interpretation prompt:** State whether the cross-country association and the within-country association point in the same direction. Explain what changes when identification comes from within-country variation rather than between-country averages.

### Question 2

**Prompt:** Use `bigimp` to examine whether income increases before or after large governance improvements. First run a two-way fixed-effects regression with per-capita GDP as the outcome, then build an event-study figure for lead/lag values from -5 to +5.

**Expected artifact:** `[figure_q2_event_study]`

**Interpretation prompt:** Describe the pre-improvement pattern and post-improvement pattern separately. Flag whether the figure looks more consistent with rising income before governance improvements, rising income after improvements, or no clear timing pattern.

### Question 3

**Prompt:** Interpret Q1 and Q2 in concise sentences. Are richer countries better governed on average? Should we expect political improvements in African countries with rapidly expanding economies?

**Expected artifact:** prose only.

**Interpretation prompt:** Separate the average-country comparison from the timing/event-study evidence. Keep the answer cautious about causality.

### Question 4

**Prompt:** Adjust the analysis so it describes the representative person rather than the representative country. Use one table, one figure, and one paragraph to describe how the answer changes.

**Expected artifacts:** `[table_q4_population_weighted]` and `[figure_q4_population_weighted]`

**Interpretation prompt:** Explain what data were added, how weighting changes the estimand, and whether populous countries change the substantive conclusion.

## Part II: Regression Discontinuity Design

### Question 5

**Prompt:** Read the introduction of Angrist and Lavy (1999). Explain the endogeneity problem in a simple OLS regression of test scores on class size. Identify possible omitted variables and state whether OLS would over- or underestimate the true effect.

**Expected artifact:** prose only.

**Interpretation prompt:** Tie the omitted-variable story to parental sorting, school resources, student background, or administrative assignment. Be explicit about the likely direction of bias.

### Question 6

**Prompt:** Plot a histogram of `school_enrollment`. Do parents appear to take Maimonides' Rule into account when choosing a school?

**Expected artifact:** `[figure_q6_enrollment_histogram]`

**Interpretation prompt:** Discuss whether there is visible bunching or manipulation around the enrollment cutoff. Connect the answer to the credibility of the running variable.

### Question 7

**Prompt:** Plot the relationship between `classize` and math scores, and between `classize` and verbal scores. Include the Maimonides Rule cutoff. What do you observe? Does the evidence justify the preference for smaller classes?

**Expected artifact:** `[figure_q7_classize_scores]`

**Interpretation prompt:** Distinguish the first-stage visual relationship between enrollment and class size from the reduced-form relationship between class size and scores. Do not make a causal claim from the raw scatter alone.

### Question 8

**Prompt:** Estimate the RD effect of crossing the enrollment cutoff of 40 on `avgmath` and `avgverb`, restricting to schools with fewer than 80 students enrolled.

#### Question 8a

**Prompt:** Manually implement local regressions on each side of the cutoff using a bandwidth of your choice. Report the coefficient, bandwidth, and effective N on each side. Justify the choice.

**Expected artifact:** `[table_q8_manual_rd]`

**Interpretation prompt:** Explain the estimand at the cutoff and why the chosen bandwidth balances local comparability against sample size.

#### Question 8b

**Prompt:** Re-estimate with `rdrobust` defaults. Report coefficient, bandwidth, effective N on each side, and 95 percent confidence interval. Compare to the manual estimate.

**Expected artifact:** `[table_q8_rdrobust]`

**Interpretation prompt:** Say whether the default robust estimate is similar in sign, magnitude, and uncertainty to the manual local-regression estimate. Explain any meaningful difference through bandwidth, weighting, or robust bias correction.

### Question 9

**Prompt:** Choose and run one falsification test, such as a density test on the running variable, a smoothness test using a predetermined covariate, or a placebo cutoff. Explain the choice, present the result, and discuss what failure would imply.

**Expected artifact:** `[table_q9_falsification]` or `[figure_q9_falsification]`

**Interpretation prompt:** State the identifying assumption being probed. If the test fails, explain why that weakens the RD design rather than treating it as a minor technical problem.

## AI Use Disclosure Reminder

Before submission, add the external AI Use Disclosure required by the Claudia SOP if any AI-assisted code, prose, debugging, interpretation, or formatting remains in the submitted `.R` file(s) or PDF. Use the course-appropriate wording and make sure Edgar personally reviews, verifies, and can explain the final work.

## Final Submission Checklist

- Both `.R` file(s) and PDF are submitted.
- Questions are numbered Q1-Q9.
- All referenced tables and figures are visible in the PDF.
- Regression tables include standard errors.
- Figures have titles, labels, and readable formatting.
- Q8 clearly states the `school_enrollment < 80` restriction.
- Q8 reports coefficient, bandwidth, effective N on each side, and confidence interval where required.
- Q9 explains why the falsification test matters.

---
Generated for: Edgar Agunias
Date: 2026-05-19
Model: GPT-5 Codex
Sources: Homework 2 assignment PDFs, Tyche agent context, Tyche feedback log, Claudia SOPs
Agent: Tyche
---
