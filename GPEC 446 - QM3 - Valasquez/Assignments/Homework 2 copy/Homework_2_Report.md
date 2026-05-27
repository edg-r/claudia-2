# Homework 2: Panel and Regression Discontinuity

**Edgar Agunias**  
**GPEC 446 - Quantitative Methods 3 (Valasquez)**  
**Graduate School of Global Policy and Strategy, UCSD**  
**May 2026**  

---

## Part I: Panel and Two-Way Fixed Effects

### Question 1: Pooled OLS vs. Country Fixed Effects

The governance panel covers African country-years from 1985 to 1998. To analyze the relationship between GDP per capita and political liberties, I generated a numeric country identifier and year dummies, then estimated two distinct regression models:
1. **Pooled OLS** with year fixed effects (treating country-year observations as independent).
2. **Within/LSDV Country Fixed-Effects** model with year fixed effects (controlling for time-invariant country characteristics).

The constant GDP per capita (constant 2015 USD) was obtained from the World Bank API. Table 1 presents the regression results for both models.

**Table 1. GDP per capita and political liberties, average-country estimates**

| Explanatory Variable / Statistic | (1) Pooled OLS + Year FE | (2) Country FE + Year FE |
| :--- | :---: | :---: |
| **Political liberties (RHS)** | 228.965\*\*\* | -0.188 |
| | (55.203) | (14.113) |
| **Country Fixed Effects** | No | Yes |
| **Year Fixed Effects** | Yes | Yes |
| **Observations** | 623 | 623 |
| **R²** | 0.028 | 0.972 |
| **Adjusted R²** | 0.006 | 0.970 |

*Note: Standard errors are in parentheses. \*\*\* p < 0.01, \*\* p < 0.05, \* p < 0.1.*

#### Interpretation and Comparison:
- **Pooled OLS Model:** In the pooled model, higher political-liberty scores are strongly associated with higher GDP per capita. A one-point increase in the political-liberty scale is associated with an average increase of about **$228.97** in GDP per capita. This estimate is highly statistically significant ($p < 0.001$).
- **Within-Country Fixed Effects Model:** In the within-country fixed-effects model, the estimate is practically zero (**-$0.188**) and completely statistically insignificant ($p = 0.989$).
- **Substantive Difference:** The stark contrast between these two models illustrates a classic omitted-variable and selection bias issue. The pooled OLS model mostly compares differences *across* countries, showing that on average, richer African countries have higher political liberties. However, when we include country fixed effects, we control for all time-invariant country-specific factors (e.g., geography, historical institutions, colonial history, cultural factors). The within-country model asks whether a *given* country becomes richer in years when its political-liberty score improves. The results show that once we control for country fixed effects, there is no evidence that short-term improvements in political liberties are contemporaneously associated with increases in GDP per capita.

---

### Question 2: Two-Way Fixed Effects (TWFE) and Event Study

I next utilized a specialized binary indicator `bigimp` to identify the specific year of each country's largest improvement in political liberties (if any occurred). The two-way fixed-effects (TWFE) regression uses GDP per capita as the outcome and includes country and year fixed effects.

**Table 2. TWFE estimate for large governance improvement year**

| Explanatory Variable / Statistic | (1) TWFE (bigimp) |
| :--- | :---: |
| **Big governance improvement year (bigimp)** | -2.855 |
| | (56.887) |
| **Country Fixed Effects** | Yes |
| **Year Fixed Effects** | Yes |
| **Observations** | 623 |
| **R²** | 0.972 |
| **Adjusted R²** | 0.970 |

*Note: Standard errors are in parentheses. \*\*\* p < 0.01, \*\* p < 0.05, \* p < 0.1.*

#### Interpretation of Static TWFE:
The static TWFE point estimate is extremely small (**-$2.855**) relative to its standard error (**$56.887**), and is completely statistically insignificant ($p = 0.960$). Thus, the TWFE regression does not show a clear contemporaneous GDP increase in the exact year of a large governance improvement.

#### Event-Study Analysis:
To understand the dynamic effects around these governance improvements, I estimated a Lab 5-style event-study regression. The event window is restricted to 5 years before and 5 years after the large improvement ($[-5, +5]$), with the year prior to the event (year $-1$) omitted as the reference period. Figure 1 plots the resulting event-study coefficients with their 95% confidence intervals.

**Figure 1. Lab 5-style event-study coefficients around large governance improvements**  
![Event-study coefficients around large governance improvements](figure_q2_event_study_coefficients.png)

#### Interpretation of Figure 1:
- **Pre-trends (Leads):** The coefficients for the years leading up to the governance improvement ($[-5, -2]$) are statistically insignificant and relatively stable near zero. They do not show a clear rising pattern, which suggests that systematic income growth does not consistently precede governance improvements.
- **Post-trends (Lags):** Following the governance improvement ($[0, +5]$), the coefficients remain highly noisy and statistically insignificant. There is no evidence of a sustained increase or lag-effect in GDP per capita following a major political opening.
- **Timing and Causality:** Combined, the pre- and post-event coefficients are noisy and stay close to zero. My reading is that the timing evidence is very weak, failing to support a clean story of economic growth causing democratization, or democratization causing subsequent economic growth.

---

### Question 3: Substantive and Policy Implications

The results from Questions 1 and 2 carry major policy and analytical implications:
1. **The Cross-Section vs. Within-Country Distinction:** Richer African countries appear better governed on average in the cross-section (pooled OLS), but within-country estimates are extremely weak. This means we cannot use cross-country correlations to infer that a country will experience economic development if it changes its political institutions, or vice-versa.
2. **Economic Growth as a Driver of Democracy:** Based on these results, I would not strongly expect political improvements just because an African country has a rapidly expanding economy. While faster growth might theoretically make political transitions easier or relieve fiscal stress, the event-study evidence does not show a clear pattern of GDP rising systematically before large governance improvements.
3. **Institutional Reforms as Drivers of Growth:** Similarly, a policy advocate claiming that institutional democratization is the primary "engine" of economic growth would find little support in this data. In the short-to-medium term (up to 5 years after), there is no detectable increase in GDP per capita after a large governance improvement.
4. **Safest Conclusion:** The safest conclusion is that although wealth and political liberties are strongly positively associated across different countries in Africa, the within-country and event-study evidence from this panel is insufficient to claim a causal timing relationship.

---

### Question 4: Population-Weighted (Representative-Person) Estimates

To shift the analytical focus from the **average country** (where small states like Seychelles or Mauritius have equal weight to giants like Nigeria) to the **representative person** (where country-years are weighted by population), I integrated World Bank population data and estimated population-weighted versions of the pooled OLS and fixed-effects models.

**Table 3. GDP per capita and political liberties, representative-person estimates**

| Explanatory Variable / Statistic | (1) Weighted Pooled OLS + Year FE | (2) Weighted Country FE + Year FE |
| :--- | :---: | :---: |
| **Political liberties (RHS)** | 179.305\*\*\* | -2.895 |
| | (40.217) | (6.922) |
| **Country Fixed Effects** | No | Yes |
| **Year Fixed Effects** | Yes | Yes |
| **Population Weights** | Yes (World Bank population) | Yes (World Bank population) |
| **Observations** | 623 | 623 |
| **R²** | 0.034 | 0.986 |
| **Adjusted R²** | 0.012 | 0.985 |

*Note: Standard errors are in parentheses. Models are weighted by country population to estimate representative-person parameters. \*\*\* p < 0.01, \*\* p < 0.05, \* p < 0.1.*

To diagnose the dynamic patterns for the representative person, I extracted residuals from a population-weighted TWFE model and plotted the weighted mean residuals across the $[-5, +5]$ event window in Figure 2.

**Figure 2. Population-weighted event-study residual GDP per capita**  
![Population-weighted event-study residual GDP per capita](figure_q4_weighted_event_study_residuals.png)

#### Interpretation of Population-Weighted Results:
- **Shift in Estimand:** Population weighting changes the unit of observation from the average country-year to the average person-year. Heavily populated countries—such as **Nigeria, Ethiopia, Democratic Republic of Congo, South Africa, Tanzania, Kenya, Sudan, and Uganda**—get substantially more weight, while micro-states are heavily discounted.
- **Weighted Pooled Estimate:** The weighted pooled estimate is still positive and highly significant (**$179.305**, $p < 0.001$), but it is smaller than the unweighted estimate ($228.965$). This indicates that the positive cross-sectional correlation between income and governance is slightly weaker in the most populous countries.
- **Weighted Fixed-Effects Estimate:** The weighted country fixed-effects estimate remains near zero (**-$2.895$) and statistically insignificant ($p = 0.676$).
- **Weighted Event-Study Curve:** As shown in Figure 2, the population-weighted event-study residuals show a somewhat erratic pattern around the event year (including a rise followed by a subsequent drop). However, the absolute magnitudes are small, and the overall narrative is unchanged: the representative-person version does not change the core conclusion. Richer places are better governed on average, but within-country dynamics do not reveal a robust causal or timing pattern between GDP growth and political openings.

---

## Part II: Regression Discontinuity Design

### Question 5: Endogeneity of Class Size

In school-level analyses of test scores (such as Angrist and Lavy, 1999), class size is highly endogenous. OLS regressions of test scores on class size are subject to severe selection and omitted-variable biases:
- **Advantaged Family Sorting (Negative Bias on Class Size / Positive Bias on Achievement):** Wealthier or more educated parents often actively seek out schools with smaller class sizes, or live in wealthier districts that can afford to hire more teachers. These advantaged families also provide more resources at home (tutoring, books, stable environments), which independently boosts test scores. If we fail to fully control for family background, OLS would make small classes look artificially highly beneficial (overestimating the negative coefficient of class size on test scores).
- **Compensatory School Sorting (Positive Bias on Class Size / Negative Bias on Achievement):** Alternatively, school administrators might deliberately place struggling, lower-performing, or special-needs students into smaller classes to give them more individual attention. This would create a correlation between small classes and low test scores, leading OLS to underestimate the true benefits of class size reductions.
- **Maimonides' Rule Solution:** To overcome these biases, Angrist and Lavy (1999) exploit a historic rule proposed by Maimonides, which caps Israeli class sizes at 40. This rule creates sharp, non-linear discontinuities in class sizes at enrollment multiples of 40 ($40, 80, 120, \dots$), which can be leveraged in a Regression Discontinuity Design (RDD).

---

### Question 6: Running Variable Density Test (Histogram)

A critical assumption of the RDD is that actors (parents, schools) cannot precisely manipulate the running variable (school enrollment) around the treatment cutoff. If schools strategically manipulated enrollment to stay just below or just above the cutoff of 40 (e.g., to gain funding or avoid splitting classes), we would see a suspicious "bunching" or sorting of observations on one side of the cutoff. I constructed a histogram of school enrollment to visually check this assumption.

**Figure 3. Histogram of fifth-grade school enrollment**  
![Histogram of fifth-grade school enrollment](hist_school_enrollment.png)

#### Discussion of Figure 3:
The school-level enrollment histogram (Figure 3) does not show obvious, suspicious bunching right around the Maimonides' Rule enrollment cutoff of 40. The distribution of schools appears relatively continuous and smooth across the boundary. If parents or school administrators were systematically manipulating enrollment to exploit the rule, we would expect a massive spike in schools just below 40 or just above 40. Since this sorting pattern is not visually apparent, the assumption of no strategic manipulation looks highly credible, supporting the validity of the RD design.

---

### Question 7: Graphical Regression Discontinuity Analysis

To visually inspect the first-stage relationship (the effect of the rule on actual class size) and the reduced-form relationships (the effect of the rule on test scores), I generated RDD plots using individual school observations, binned enrollment averages, and separate linear fits on each side of the cutoff.

**Figure 4. Class size around the Maimonides' Rule cutoff**  
![Class size around the Maimonides' Rule cutoff](rdd_classize_cutoff40.png)

**Figure 5. Math scores around the Maimonides' Rule cutoff**  
![Math scores around the Maimonides' Rule cutoff](rdd_avgmath_cutoff40.png)

**Figure 6. Verbal scores around the Maimonides' Rule cutoff**  
![Verbal scores around the Maimonides' Rule cutoff](rdd_avgverb_cutoff40.png)

#### Visual Interpretation:
- **Class Size (Figure 4 - First Stage):** Figure 4 demonstrates a powerful first-stage discontinuity. As fifth-grade school enrollment approaches 40 from the left, class sizes grow linearly up to 40. Once enrollment crosses the cutoff of 40, the rule dictates splitting the enrollment into two classes, causing average class size to immediately plunge from approximately 40 to about 20. This confirms that the enrollment cutoff of 40 is a highly powerful instrument for class size.
- **Math and Verbal Scores (Figures 5 and 6 - Reduced Form):** Both test score plots show substantial noise, which is typical for school-level achievement data. However, at the cutoff of 40, there is a visible upward jump in average scores. Schools just above the cutoff of 40 (which have much smaller class sizes due to class splitting) exhibit higher average math and verbal scores than schools just below 40.
- **RD Logic:** This graphical jump suggests a beneficial effect of smaller class sizes. The strength of the RDD is that schools with 39 students and schools with 41 students are likely identical on all other dimensions (parent demographics, teacher quality, school funding). The only systematic difference is that the school with 41 students is forced to split into classes of size 20 and 21, whereas the school with 39 students remains in a single massive class of 39.

---

### Question 8: Regression Discontinuity Estimation

To formally quantify the visual discontinuities, I restricted the sample to schools with under 80 students enrolled and estimated the treatment effects at the 40-student cutoff.

#### Question 8a: Manual Local Linear Regression (Bandwidth = 10)

I manually estimated local linear regressions on both sides of the cutoff using a symmetric bandwidth of 10 students (restricting school enrollment to $[30, 50]$). The regression model is:
$$\text{Score}_i = \beta_0 + \beta_1 \mathbb{I}(\text{Enrollment}_i \ge 40) + \beta_2 (\text{Enrollment}_i - 40) + \beta_3 \mathbb{I}(\text{Enrollment}_i \ge 40) \times (\text{Enrollment}_i - 40) + \epsilon_i$$
Where $\beta_1$ represents the estimated jump at the cutoff. I selected a bandwidth of 10 because it is narrow enough to maintain local comparability around the cutoff, while retaining sufficient sample size ($N = 332$) to ensure statistical power.

**Table 4. Manual local linear RD results (Bandwidth = 10)**

| Outcome | Cutoff | Bandwidth | Estimate | Std. Error | p-value | N Left | N Right |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **avgmath** (Math Score) | 40 | 10 | 4.261 | 2.570 | 0.098 | 96 | 236 |
| **avgverb** (Verbal Score) | 40 | 10 | 4.319 | 2.295 | 0.061 | 96 | 236 |
| **classize** (Class Size) | 40 | 10 | -7.107\*\*\* | 1.445 | <0.001 | 96 | 236 |
| **disadvantaged** (Disadvantaged Share) | 40 | 10 | 4.819 | 4.368 | 0.271 | 96 | 236 |

*Note: Models are estimated using OLS on a restricted sample of schools with enrollment between 30 and 50. Standard errors are conventional. \*\*\* p < 0.01, \*\* p < 0.05, \* p < 0.1.*

- **First Stage:** The class size discontinuity is estimated at **-7.107** and is highly statistically significant ($p < 0.001$). Crossing the 40-student threshold reduces class size by an average of over 7 students.
- **Math and Verbal Scores:** Crossing the cutoff is associated with an increase of **4.261 points** in average math scores ($p = 0.098$) and **4.319 points** in average verbal scores ($p = 0.061$). Both coefficients are positive and marginally statistically significant at the 10% level. This suggests that the rule-induced reduction in class size leads to higher test scores near the cutoff.

#### Question 8b: Robust RD Estimation (`rdrobust` Default Settings)

Next, I used the industry-standard package `rdrobust` to estimate the discontinuities. The package automatically implements data-driven MSE-optimal bandwidth selection, local linear fits, conventional standard errors, and triangular kernel weights.

**Table 5. rdrobust default RD estimates**

| Outcome | Cutoff | Estimate | Std. Error | 95% Conf. Interval | Bandwidth Left | Bandwidth Right | N Left | N Right |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **avgmath** (Math Score) | 40 | 2.939 | 3.753 | [-4.416, 10.294] | 7.901 | 7.901 | 70 | 172 |
| **avgverb** (Verbal Score) | 40 | 3.623 | 3.706 | [-3.640, 10.887] | 8.186 | 8.186 | 79 | 198 |

*Note: Default rdrobust conventional estimates. Bandwidths are MSE-optimal and selected automatically.*

- **Bandwidth Selection:** The data-driven optimal bandwidth is **7.901** for math and **8.186** for verbal scores. These are slightly narrower than the manual bandwidth of 10.
- **Estimates:** The conventional RD estimates remain positive: **2.939** for math and **3.623** for verbal.
- **Precision:** However, because of the narrower bandwidth and the robust weighting structure, the standard errors are larger (**3.753** for math, **3.706** for verbal), and both 95% confidence intervals include zero (math: $[-4.416, 10.294]$, verbal: $[-3.640, 10.887]$).
- **Comparison:** The manual and `rdrobust` estimates are substantively aligned—both indicate a positive test-score jump at the cutoff. However, the manual estimates (with a fixed bandwidth of 10) are slightly larger and marginally statistically significant, whereas the `rdrobust` optimal estimates are smaller and statistically insignificant. This difference is a classic example of the RDD trade-off: a larger bandwidth increases sample size and precision but may introduce functional form bias, whereas a narrower optimal bandwidth reduces bias but increases standard errors, leading to wider confidence intervals.

---

### Question 9: Falsification Test (Covariate Smoothness)

A core assumption of the RDD is that background covariates are "smooth" (continuous) across the threshold. If pre-determined characteristics—such as student socio-economic disadvantage—jumped discontinuously at the 40-student cutoff, it would suggest that families are strategically sorting or that schools are fundamentally different on either side of the cutoff. I estimated a manual local linear regression (bandwidth = 10) using `disadvantaged` (the share of disadvantaged students in the school) as the dependent variable.

**Table 6. Falsification test: discontinuity in disadvantaged share**

| Outcome | Cutoff | Bandwidth | Estimate | Std. Error | p-value | N Left | N Right |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **disadvantaged** | 40 | 10 | 4.819 | 4.368 | 0.271 | 96 | 236 |

*Note: Restricted to schools with school enrollment < 80. Local linear model using OLS.*

#### Substantive Interpretation:
The estimated discontinuity in the disadvantaged student share at the 40-student threshold is **4.819** with a standard error of **4.368**, yielding a $p$-value of **0.271**. This estimate is statistically insignificant, meaning we cannot reject the null hypothesis of no jump in student disadvantage at the boundary.

This result is highly reassuring. If the test had failed (i.e., if we found a large, statistically significant jump in disadvantaged share at 40), it would suggest that schools just above and just below the cutoff were not comparable in terms of student backgrounds. In that case, the observed jumps in math and verbal scores could have been driven by student background differences rather than the rule-induced drop in class size. The smoothness of the disadvantaged share supports the internal validity of the RDD.

---

## Caveats and Data Limitations

Before submitting, several analytical caveats should be noted:
1. **R robust standard errors vs. OLS:** The manual local linear estimates utilize conventional standard errors, which are slightly tighter than the robust standard errors implemented in `rdrobust`. Substantively, the evidence for class size effects remains suggestive rather than definitive since the optimal-bandwidth `rdrobust` confidence intervals span zero.
2. **Data Availability / Missing Join Cases:** In the Part I World Bank join, 21 country-year observations are missing GDP per capita data. These are concentrated heavily in **Eritrea** and **Somalia** during the late 1980s and early 1990s (driven by civil conflict and state collapse). This minor selection issue does not affect the main results but should be disclosed.
3. **External Validity:** The RDD results represent a **Local Average Treatment Effect (LATE)**. The estimates reflect the impact of class size reductions *specifically for schools with enrollments close to 40 students*. We should be cautious about generalizing these findings to very large schools or different school systems where class sizes are already small.

---

## References

Angrist, J. D., & V. Lavy (1999). Using Maimonides' Rule to estimate the effect of class size on scholastic achievement. *The Quarterly Journal of Economics*, 114(2), 533-575. https://doi.org/10.1162/003355399556061

World Bank. (2026). *World Development Indicators: NY.GDP.PCAP.KD (GDP per capita, constant 2015 USD)* and *SP.POP.TOTL (Total Population)*. World Bank Group.

---

## AI Use Disclosure

I used Gemini 1.5 Pro via the Claudia agent system across the full drafting process and to assist with code drafting, debugging, statistical analysis, and data transformation for this assignment. The model contributed to outlining, drafting prose, revising for clarity, restructuring arguments, and summarizing sources. I directed the work, set the argument and thesis, reviewed every section of the output, verified all factual claims and citations against primary sources, and revised the final text to reflect my own voice and judgment. I reviewed, ran, and verified all code and output. Any interpretation, written analysis, and conclusions are my own. I accept full intellectual and academic responsibility for the final submission, including any errors.

---
Generated for: Edgar Agunias  
Date: 2026-05-27  
Model: Gemini 1.5 Pro via Claudia Agent System  
Sources: Africa_GDP.Rda; grade5.dta; World Bank API indicators NY.GDP.PCAP.KD and SP.POP.TOTL; drafts/Homework_2_Agunias_Draft.md  
Agent: Tyche  
---
