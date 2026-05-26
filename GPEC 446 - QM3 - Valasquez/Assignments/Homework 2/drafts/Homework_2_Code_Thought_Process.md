# Homework 2 Code Thought Process

This companion explains the logic behind the Homework 2 answers and why the R scripts are organized the way they are. It is meant to help Edgar explain the work in office hours without turning into line-by-line code commentary.

## Overall Workflow

Homework 2 has two different causal-inference designs.

Part I uses a country-year panel for African countries from 1985 to 1998. The code asks whether political liberties and GDP per capita move together, first through pooled comparisons, then through country fixed effects, two-way fixed effects (TWFE), event-study timing, and population-weighted versions. The key distinction is between comparing different countries to each other and comparing a country to itself over time.

Part II uses a regression discontinuity (RD) design around the Maimonides' Rule cutoff at 40 students. The code asks whether schools just above and just below the cutoff look similar except for the rule-induced class-size change. The workflow moves from visual checks to manual local regressions, then to `rdrobust`, and ends with a falsification test.

At a high level, the scripts are structured this way:

- Set paths and output folders so the analysis can be rerun from RStudio or the terminal.
- Load raw data and create clean analysis variables.
- Export intermediate tables and figures so every answer in the draft has a visible source.
- Keep Part I and Part II separate because they use different data, designs, assumptions, and packages.
- Write notes files that summarize the results for final-report integration.

## Q1: Pooled OLS vs. Within-Country Fixed Effects

### Goal

Q1 asks whether political liberties are associated with GDP per capita in the African country-year panel. The main conceptual goal is to separate an across-country relationship from a within-country relationship.

### General Strategy

The code estimates two models:

- Pooled OLS with year fixed effects.
- A country fixed-effects model with year fixed effects.

The pooled model compares richer and poorer country-years after controlling for common year shocks. The fixed-effects model compares each country to itself over time, which removes permanent country differences such as geography, colonial history, resource endowments, or long-run institutions.

### Macro-Level Pseudocode

- Load the governance panel from `Africa_GDP.Rda`.
- Keep the assignment years, 1985-1998.
- Match class-file country names to World Bank country names.
- Download GDP per capita from the World Bank.
- Join GDP per capita to the governance panel.
- Create a numeric country identifier and a year factor.
- Estimate:
  - `GDP per capita = political liberties + year effects`
  - `GDP per capita = political liberties + country effects + year effects`
- Export only the political-liberties coefficient rows into the Q1 table.

### Why This Approach Makes Sense

The question is not just whether richer countries have better governance. That is the easy cross-sectional pattern. The harder question is whether changes in governance within the same country line up with changes in income. Country fixed effects help answer that second question by holding constant anything about a country that does not change over the period.

Year fixed effects are included in both models because African countries may share common shocks in a given year, such as commodity-price changes, debt crises, international reforms, or regional macroeconomic changes.

### How to Interpret the Output

The pooled estimate is positive and statistically significant: higher political-liberty scores are associated with higher GDP per capita across country-years. The fixed-effects estimate is almost zero and statistically insignificant.

The office-hours explanation is: "When I compare different countries, better-governed places are richer. But when I compare a country to itself over time, years with higher political liberty are not clearly richer after controlling for country and year fixed effects."

## Q2: TWFE and Event Study Around Large Governance Improvements

### Goal

Q2 asks whether GDP per capita changes around a country's largest political-liberty improvement. This moves from a general association to a timing question.

### General Strategy

The code uses `bigimp` to identify the year of a country's largest governance improvement. It estimates a TWFE model for the exact improvement year and then builds a Lab 5-style event-study figure using years before and after the event.

### Macro-Level Pseudocode

- Use the cleaned Part I panel from Q1.
- Replace missing `bigimp` values with zero so the event indicator is usable.
- Within each country, identify the event year where `bigimp == 1`.
- Create `leadlag = year - event_year`.
- Estimate:
  - `GDP per capita = big improvement indicator + country effects + year effects`
- Remove country and year fixed effects from GDP per capita to get residual GDP.
- Keep observations from five years before to five years after the event.
- Relevel event time so year -1 is the omitted reference period, matching the Lab 5 template.
- Estimate one TWFE coefficient for each event-time lead and lag, controlling for country and year fixed effects.
- Plot the event-time coefficients with 95% confidence intervals.

### Why This Approach Makes Sense

TWFE is useful because it compares countries to themselves while also netting out common year shocks. The event-study graph adds timing information that a single coefficient cannot show. If GDP rises before governance improves, that would support the idea that economic growth may precede political improvement. If GDP rises after governance improves, that would be more consistent with governance improvement coming first.

The submitted event-study plot uses event-time coefficients rather than residual means. The script still keeps residual means as a diagnostic output, but the main Q2 figure now mirrors Lab 5 more directly.

### How to Interpret the Output

The TWFE `bigimp` coefficient is very small relative to its standard error. The event-study plot is noisy and does not show a strong pre-event or post-event pattern.

The interpretation is cautious: the timing evidence does not clearly show that economic growth systematically precedes political improvement, and it also does not clearly show that political improvement causes later GDP gains.

## Q3: Substantive Interpretation of Q1 and Q2

### Goal

Q3 asks for a substantive conclusion from the Part I evidence: should we expect political improvement just because an African country's economy is rapidly expanding?

### General Strategy

The answer compares what Q1 and Q2 can and cannot support. Q1 shows the difference between across-country association and within-country association. Q2 checks whether income changes are timed around large governance improvements.

### Macro-Level Pseudocode

- Read the Q1 pooled estimate.
- Read the Q1 fixed-effects estimate.
- Read the Q2 TWFE estimate.
- Inspect the Q2 event-study figure.
- Translate the pattern into a causal-interpretation paragraph.

### Why This Approach Makes Sense

This question is mostly interpretation rather than new modeling. The code structure keeps the empirical evidence visible: Q1 supplies the association, and Q2 supplies the timing check. That prevents the answer from overstating a causal story just because the pooled model is positive.

### How to Interpret the Output

The pooled comparison says richer countries tend to have better governance. The fixed-effects and event-study results do not show that a given country becomes richer when governance improves, or that economic growth clearly comes before political improvement.

The best answer is: income and governance are positively associated across countries, but this homework evidence is not strong enough to claim that rapid growth alone should produce political improvement.

## Q4: Population-Weighted, Representative-Person Estimates

### Goal

Q4 asks how the results change when the analysis represents the average person rather than the average country-year.

### General Strategy

The code adds World Bank population data and uses population as regression weights. This gives more influence to larger countries such as Nigeria, Ethiopia, Democratic Republic of Congo, South Africa, Tanzania, Kenya, Sudan, and Uganda.

### Macro-Level Pseudocode

- Download population from the World Bank.
- Join population to the same country-year panel used in Q1-Q2.
- Drop rows with missing or zero population for the weighted regressions.
- Estimate population-weighted versions of:
  - pooled OLS with year effects
  - country fixed effects with year effects
- Estimate a population-weighted residual event-study.
- Export a weighted table and weighted event-study figure.

### Why This Approach Makes Sense

Unweighted country-year regressions treat Seychelles and Nigeria as equally important observations. That answers an "average country" question. Population weighting answers a different question: what does the relationship look like for the average person living in the African country-years in the sample?

This matters because a pattern driven by many small countries may not describe the experience of most people.

### How to Interpret the Output

The weighted pooled estimate remains positive but is smaller than the unweighted pooled estimate. The weighted fixed-effects estimate remains close to zero and statistically insignificant. The weighted event-study also does not create a clear causal timing pattern.

The conclusion is that population weighting changes the estimand and the size of the pooled coefficient, but not the main substantive takeaway.

## Q5: Why Simple OLS on Class Size Is Endogenous

### Goal

Q5 asks why an ordinary regression of test scores on class size may be biased in the Angrist and Lavy class-size setting.

### General Strategy

This is a conceptual setup for the RD design. The answer explains why class size is not randomly assigned and why omitted variables may be correlated with both class size and achievement.

### Macro-Level Pseudocode

- Identify the outcome: student test scores.
- Identify the treatment variable: class size.
- Ask whether class size is randomly assigned.
- List omitted factors that affect scores and may also affect class size:
  - parent resources
  - neighborhood income
  - school quality
  - teacher quality
  - peer composition
  - disadvantaged share
- Explain the likely direction of bias.

### Why This Approach Makes Sense

The RD design only matters because naive OLS is not credible. If smaller classes are concentrated in advantaged schools, then simple OLS may attribute high achievement to small classes even when part of the difference comes from family or school advantage. If schools compensate weaker students with smaller classes, the bias could go the other way.

The code for Part II does not try to solve Q5 by running naive OLS because the question is asking for the identification problem. The later RD code is the solution to that problem.

### How to Interpret the Output

There is no statistical table for Q5. The interpretation is conceptual: simple OLS probably mixes the effect of class size with nonrandom differences among schools and students. The most intuitive bias is that OLS overstates the benefit of smaller classes if advantaged families sort into schools with smaller classes.

## Q6: Histogram of School Enrollment Near the Cutoff

### Goal

Q6 asks whether the running variable, school enrollment, appears manipulated around the cutoff.

### General Strategy

The code plots a histogram of school enrollment and marks the cutoff at 40. The visual question is whether there is suspicious bunching just below or above 40.

### Macro-Level Pseudocode

- Load `grade5.dta`.
- Keep key variables such as school enrollment, class size, scores, and covariates.
- Plot a histogram of `school_enrollment`.
- Add a vertical line at 40.
- Inspect whether the distribution piles up around the cutoff.

### Why This Approach Makes Sense

Regression discontinuity depends on the idea that units cannot precisely manipulate which side of the cutoff they fall on. If families or schools strategically sorted around 40 to get smaller classes, then schools just below and above 40 might not be comparable.

The histogram is a first-pass diagnostic. It does not prove the RD assumption, but it can reveal obvious manipulation.

### How to Interpret the Output

The histogram does not show obvious bunching right around 40. That makes the RD design more plausible. The careful interpretation is: "I do not see strong visual evidence of manipulation, but this is a diagnostic rather than a proof."

## Q7: First Stage and Outcome Plots Around the Cutoff

### Goal

Q7 asks for visual evidence around the Maimonides' Rule cutoff. The class-size plot checks whether the rule actually changes class size. The score plots check whether math and verbal scores change at the same cutoff.

### General Strategy

The code makes separate RD-style plots for class size, math scores, and verbal scores. It restricts the visual focus to schools with enrollment below 80 and fits separate linear trends on each side of 40.

### Macro-Level Pseudocode

- Create `enrollment_centered = school_enrollment - 40`.
- Create `above_cutoff = 1` when enrollment is at least 40.
- Restrict plots to enrollment below 80.
- For each outcome:
  - plot raw observations with transparency
  - add binned means by exact enrollment
  - fit a linear trend below 40
  - fit a linear trend at or above 40
  - add a vertical line at 40
- Save one plot each for class size, math, and verbal scores.

### Why This Approach Makes Sense

In an RD design, the key evidence is the jump at the cutoff. The first-stage plot is especially important: if class size does not fall at 40, then the rule is not creating the treatment variation the design needs. The outcome plots show whether test scores move at the same point where class size changes.

Separate linear fits on each side are useful because RD does not assume one single line through the whole sample. It asks whether there is a discontinuity at the cutoff after allowing the relationship with enrollment to differ on either side.

### How to Interpret the Output

The class-size plot shows the expected drop at 40: once enrollment crosses 40, the rule tends to create a second class, lowering average class size. The score plots are noisier but show higher math and verbal scores just above the cutoff in the local fits.

The correct interpretation is local and cautious: the plots are consistent with a smaller-class benefit near the cutoff, but the formal RD estimates in Q8 are needed before making the causal statement.

## Q8a: Manual Local Linear RD

### Goal

Q8a asks for a manual RD estimate around the cutoff. The idea is to estimate the jump in test scores at 40 using schools close to the cutoff.

### General Strategy

The code restricts to schools with enrollment below 80, then uses a 10-student bandwidth around 40. It estimates a local linear model with an intercept jump at the cutoff and separate slopes on each side.

### Macro-Level Pseudocode

- Keep only observations with `school_enrollment < 80`.
- Define a bandwidth of 10 students.
- Keep observations with `abs(school_enrollment - 40) <= 10`.
- Estimate, separately for math and verbal:
  - outcome = above cutoff
  - plus centered enrollment
  - plus interaction between above cutoff and centered enrollment
- Interpret the `above_cutoff` coefficient as the jump at 40.
- Report estimate, standard error, p-value, and sample size on each side.

### Why This Approach Makes Sense

The bandwidth keeps the comparison local. Schools with enrollment 35 and 45 are more likely to be comparable than schools with enrollment 10 and 75. The interaction term allows the slope between enrollment and scores to differ below and above 40, which is the local linear RD idea.

Centering enrollment at 40 matters because it makes the intercept jump directly interpretable at the cutoff. Without centering, the treatment coefficient would be harder to read.

### How to Interpret the Output

The manual estimates are positive for both math and verbal scores, about 4.3 points. This means observations just above 40 score higher than observations just below 40 after fitting local linear trends. Because crossing 40 lowers class size, the positive score jump is consistent with smaller classes improving scores near the cutoff.

The estimates are suggestive rather than definitive because the p-values are near conventional thresholds and the design is local to schools near 40.

## Q8b: `rdrobust` Default RD Estimates

### Goal

Q8b asks for RD estimates using a standard RD package rather than a fully manual specification.

### General Strategy

The code uses `rdrobust` with its default bandwidth and inference choices. It reports the conventional estimate, standard error, confidence interval, selected bandwidths, and effective sample sizes.

### Macro-Level Pseudocode

- Keep the same below-80 sample.
- For each score outcome:
  - set `x = school_enrollment`
  - set `y = avgmath` or `avgverb`
  - drop missing values
  - run `rdrobust(y, x, c = 40)`
  - extract estimate, standard error, confidence interval, bandwidths, and N
- Export the results table.

### Why This Approach Makes Sense

Manual RD estimates are transparent, but package-based RD is useful because it applies standard bandwidth selection, weighting, and inference routines. Comparing the manual and `rdrobust` results helps show whether the conclusion depends heavily on the hand-chosen bandwidth.

The script includes a blocker path if `rdrobust` is unavailable so the rest of the analysis can still run. In the current output, `rdrobust` did run and produced estimates.

### How to Interpret the Output

The `rdrobust` estimates are positive for both math and verbal scores, like the manual estimates, but they are smaller and less precise. Both confidence intervals include zero.

The office-hours interpretation is: "The sign is consistent across manual and package estimates, but `rdrobust` uses a narrower data-driven bandwidth and the uncertainty is large. I would describe the evidence as suggestive, not conclusive."

## Q9: Falsification Test Using Disadvantaged Share

### Goal

Q9 asks for a falsification or validity check. The code tests whether a predetermined covariate jumps at the cutoff.

### General Strategy

The code reuses the manual local RD function, but changes the outcome from test scores to `disadvantaged`. If student disadvantage jumps at 40, then schools just below and just above the cutoff may differ in composition, which would weaken the RD design.

### Macro-Level Pseudocode

- Use the same below-80 sample and bandwidth of 10.
- Set the outcome to `disadvantaged`.
- Estimate the same local linear RD model:
  - disadvantaged = above cutoff + centered enrollment + interaction
- Report the jump, standard error, p-value, and sample sizes.
- Interpret whether the cutoff appears to change student composition.

### Why This Approach Makes Sense

Class size can change at the cutoff because of Maimonides' Rule. But predetermined student characteristics should not change discontinuously at the cutoff if the RD comparison is valid. A jump in disadvantage would suggest that the test-score jump might reflect different student backgrounds rather than class size.

This is why Q9 is a falsification test: it looks for a discontinuity where there should not be one.

### How to Interpret the Output

The estimated jump in disadvantaged share is not statistically significant. That is reassuring because it does not show a clear composition break at the cutoff.

The correct wording is careful: the test supports the RD design, but it does not prove that every possible confounder is smooth. It only says this observed covariate does not show a clear discontinuity in the current local window.

## Final Explanation to Keep in Mind

The code is organized around identification, not just computation. Part I repeatedly asks whether a pooled association survives stricter comparisons within countries and around timing events. Part II asks whether a rule-created discontinuity can isolate class-size variation from ordinary school and family sorting.

For office hours, Edgar can describe the project in one sentence:

"Part I shows that cross-country income-governance associations weaken once I use within-country and timing comparisons, while Part II uses the Maimonides cutoff as a local source of class-size variation and finds suggestive but imprecise positive score effects."

---
Generated for: Edgar Agunias
Date: 2026-05-19
Model: GPT-5 Codex
Sources: Homework_2_Agunias_Draft.md; Homework_2_Part_I_panel.R; Homework_2_Part_II_rdd.R; PART_I_NOTES.md; PART_II_NOTES.md; README.md; Tyche agent context and feedback; Claudia SOPs
Agent: Tyche
---
