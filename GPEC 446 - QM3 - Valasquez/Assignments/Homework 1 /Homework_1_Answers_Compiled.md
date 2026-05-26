# GPEC 446 Homework 1 Answers

Edgar Agunias  
GPEC 446 - Quantitative Methods 3  
April 2026

## Opportunity Atlas

### Question 1

I chose **New Orleans**. Looking at the Opportunity Atlas map, the main pattern is clustering: tracts with higher average child income tend to appear near other higher-opportunity tracts, while lower-opportunity tracts are also grouped together. The income outcomes are not evenly spread across the city. There is large variation across neighborhoods, which suggests that upward mobility differs substantially within the same commuting zone.

### Question 2

For the tract comparison, I selected tract **22071012102** in New Orleans.

[table_q12.html]

This tract has upward mobility of about **$72,747** for children whose parents were at the 25th percentile. The New Orleans average is about **$30,615**, so the selected tract is about **$42,133 above** the city average. The standard deviation across New Orleans tracts is about **$8,114**, compared with about **$7,052** for Louisiana excluding the selected tract. This shows that New Orleans has especially large within-city variation in opportunity: the city average hides very different neighborhood-level outcomes.

### Question 3

![Poverty and upward mobility across selected cities](city_poverty_mobility.png)

[table_q3.html]

The association between tract poverty in 1990 and upward mobility is negative in all four cities. Higher-poverty tracts are associated with lower adult income for children whose parents were at the 25th percentile. The relationship is strongest in Chicago and New York, where the poverty coefficients are more negative, and somewhat weaker in Los Angeles and New Orleans. So the direction of the relationship is consistent across cities, but the size of the association differs.

### Question 4

The omitted variable is racial composition, measured by the dummy variable `majority_non_white`, which equals 1 when `share_white2000 < 0.5`.

[table_q4_ovb.html]

The omitted-variable-bias logic is:

```text
Bias = effect of omitted variable on Y x relationship between X and omitted variable
```

Here, poverty is the main independent variable, upward mobility is the outcome, and majority-non-white status is the omitted variable. In New Orleans, higher-poverty tracts are more likely to be majority non-white, and majority-non-white tracts have lower predicted mobility after controlling for poverty. Therefore, omitting racial composition should make the poverty coefficient too negative.

That is what the results show. The naive poverty coefficient is **-0.339**, while the controlled poverty coefficient is **-0.219**. The predicted omitted-variable bias is **-0.120**, which matches the actual coefficient change of **-0.120**. After adding the racial-composition control, the poverty coefficient becomes less negative, exactly as the OVB formula predicts.

### Question 5

[table_q5.html]

The interaction model tests whether the poverty slope differs between majority-white and majority-non-white tracts.

The model is:

```text
mobility = beta0 + beta1 poverty + beta2 majority_non_white
           + beta3 poverty x majority_non_white
```

In the interaction model, the poverty coefficient of **-0.442** is the poverty slope for the reference group, which is majority-white tracts. That means that, among majority-white tracts, a 1 percentage point increase in poverty is associated with about **$442 lower** child income.

The interaction coefficient is **+0.306**. This means the poverty slope is 0.306 less negative in majority-non-white tracts. The implied poverty slope for majority-non-white tracts is:

```text
-0.442 + 0.306 = -0.136
```

So, in majority-non-white tracts, a 1 percentage point increase in poverty is associated with about **$136 lower** child income. This does **not** support the hypothesis that poverty is especially harmful in majority-non-white tracts. In this model, the negative poverty association is stronger among majority-white tracts. However, the majority-non-white coefficient is still strongly negative, meaning majority-non-white tracts have a lower baseline predicted mobility level.

### Question 6

These models should not be interpreted causally. Poverty and racial composition are not randomly assigned across neighborhoods. Other neighborhood characteristics could affect both poverty and child outcomes, including school quality, housing segregation, public transit access, local labor markets, environmental exposure, policing, and family sorting into neighborhoods. Adding one control improves the model, but it does not solve the broader endogeneity problem. The results are best interpreted as associations.

### Questions 7-9

[table_q79.html]

Adding `factor(cz)` includes a dummy variable for each commuting zone. This is analogous to Dale and Krueger's application-group strategy because it changes the comparison group. Dale and Krueger compared students who applied to the same set of colleges. Here, commuting-zone fixed effects compare tracts within the same commuting zone, holding constant broad city-level factors.

The "choice set" equivalent is the commuting zone: families and children are being compared within the same regional labor market and city environment rather than across very different cities.

The poverty coefficient changes from **-0.293** in the national pooled model to **-0.260** with commuting-zone fixed effects. The majority-non-white coefficient changes from **-3.310** to **-5.614**. This means that some of the poverty association reflected cross-city differences, but substantial within-city tract-level differences remain. The stronger majority-non-white coefficient with fixed effects suggests that racial-composition differences within commuting zones are strongly associated with mobility gaps.

## Open Question

[table_open_urban_rural_regression.html]

![Average mobility by population-density decile](urban_density_deciles.png)

Using population density as a proxy for urban versus rural status, the regression evidence does not show that dense urban tracts automatically provide higher upward mobility. In the simple regression, the urban-proxy coefficient is **-1.358**, meaning top-density-quartile tracts have about **$1,358 lower** predicted mobility than bottom-density-quartile tracts. After adding poverty and majority-non-white status, the urban coefficient briefly becomes positive (**0.875**), but the preferred within-commuting-zone model is negative again: **-1.441**. This means that, comparing tracts within the same commuting zone and holding poverty and majority-non-white status constant, urban-proxy tracts have about **$1,441 lower** predicted mobility than rural-proxy tracts. The largest negative predictor in the controlled models is majority non-white status: in the fixed-effects model, majority-non-white tracts are associated with **$5,295 lower** predicted mobility. Poverty also matters, with each 1 percentage point increase in poverty associated with about **$218 lower** predicted mobility in the fixed-effects model. The decile figure also shows that mobility does not rise steadily with density. Overall, the urban-rural distinction by itself is too simple: mobility appears more strongly related to neighborhood poverty and racial composition than to density alone.

## Instrumental Variable

### Question 10

I created `same_gender`, a dummy variable equal to 1 if the first two children are the same gender and 0 otherwise. This is a plausible instrument for having a third child because parents with two children of the same gender may be more likely to try for a third child in order to have a mixed-gender set of children.

The instrument is plausible because the gender composition of the first two children is close to random, and it affects the probability of having more children. The key exclusion restriction is that the gender mix of the first two children affects maternal labor supply only through its effect on the probability of having a third child. That assumption is not directly testable, but it is the identifying assumption behind the Angrist and Evans design.

### Question 11

[table_iv_manual_2sls.html]

The first-stage regression shows that same-gender first two children increase the probability of having a third child by about **6.7 percentage points**. The reduced-form regression is negative, meaning the same-gender instrument is associated with lower maternal work. The manual second-stage estimate is **-6.033**, which means that an additional child is associated with lower maternal labor supply for the compliers whose fertility was affected by the same-gender instrument.

Because the assignment asks for the fitted-values version of 2SLS rather than `ivreg()`, the table reports the manual second-stage regression. The point estimate is the IV estimate, but the standard errors are the manual-regression standard errors rather than fully corrected IV standard errors.

## Code Understanding Sufficiency Test

[table_code_understanding.html]

The libraries used are:

- `dplyr`: used to clean, filter, group, and summarize data.
- `ggplot2`: used to create scatter plots and line plots.
- `readr`: used to import the CSV file.
- `stargazer`: used to make regression tables.
- `AER`: used to load the `Fertility2` data.

The function table lists 15 functions used in the code and explains what each one does.

## References

Angrist, J. D., & Evans, W. N. (1998). Children and their parents' labor supply: Evidence from exogenous variation in family size. *American Economic Review, 88*(3), 450-477.

Angrist, J. D., & Pischke, J.-S. (2015). *Mastering 'Metrics: The path from cause to effect*. Princeton University Press.

Dale, S. B., & Krueger, A. B. (2002). Estimating the payoff to attending a more selective college: An application of selection on observables and unobservables. *Quarterly Journal of Economics, 117*(4), 1491-1527.

Opportunity Insights. (2018). *Opportunity Atlas*. https://www.opportunityatlas.org/

## AI Use Disclosure

I used GPT-5 via the Claudia agent system (OpenAI) to assist with code drafting, debugging, statistical analysis, and compiling the answer document for this assignment. I reviewed, ran, and verified the code and output. Any interpretation, written analysis, and conclusions are my own. I accept full intellectual and academic responsibility for this submission, including any errors.

---
Generated for: Edgar Agunias
Date: 2026-04-27
Model: GPT-5
Sources: Homework_1_Codex.R, atlas.csv, Homework_1_Instructions.docx, generated Homework 1 HTML tables and PNG figures
Agent: Tyche / Claudia
---
