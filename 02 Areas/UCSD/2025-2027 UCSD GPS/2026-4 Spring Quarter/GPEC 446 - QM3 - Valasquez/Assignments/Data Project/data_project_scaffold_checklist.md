# GPEC 446 — Causal Inference Independent Data Project Scaffold & Method Checklist

This document serves as the academic blueprint and execution checklist for the upcoming **Causal Inference Independent Data Project** (due Sunday, June 7, 2026, at 23:59 PM America/Los_Angeles, weighing 25% of the final grade).

---

## 1. Project Overview & Core Requirements

The Data Project is an independent empirical research paper applying the quantitative methods covered in GPEC 446 to a real-world policy or economic question. It demands formulating a clear causal research question, executing a robust statistical analysis in R, performing diagnostic tests, and interpreting the findings in a professional, academic format.

### Key Deliverables & Guidelines
* **Empirical Focus:** Causal identification, not descriptive association. Your research design must defend why your estimates represent a causal policy impact, not a spurious correlation.
* **Method Choice:** Choose at least one (or a combination) of the core GPEC 446 strategies:
  * Randomized Controlled Trial (RCT) / Block Randomization (Gerber & Green Ch. 3–4)
  * OLS with Selection Controls & OVB Diagnosis (AP Ch. 1–2)
  * Instrumental Variables / Two-Stage Least Squares (2SLS) (AP Ch. 3)
  * Differences-in-Differences (DiD) / Two-Way Fixed Effects (TWFE) (AP Ch. 5; Wooldridge Ch. 13–14)
  * Regression Discontinuity Design (RDD) (AP Ch. 4)
  * Matching or Synthetic Control Methods (Week 6 Readings)
* **Code Standard:** Replicable, clean R script that processes raw data, runs models, and exports publication-ready tables (`stargazer`) and figures (`ggplot2`).
* **Writing Policy:** **100% individual own-voice prose.** AI tools are permitted for coding support, statistical debugging, and concept clarification, but generating written narrative responses with AI is strictly prohibited under the UCSD Office of Academic Integrity.

---

## 2. Structural Scaffold (Paper Blueprint)

Use the following 9-section structure to draft your final paper. This matches professional standards in applied econometrics and program evaluation.

### Section 1: Abstract (approx. 150 words)
* **Goal:** A self-contained summary of the paper.
* **Content:**
  * Define the policy or economic question.
  * State the core data source and sample size.
  * Name the empirical research design (e.g., "Using a staggered Difference-in-Differences strategy...").
  * Present the primary causal estimate with statistical significance.
  * State the policy implication.

### Section 2: Introduction (approx. 1 to 1.5 pages)
* **Goal:** Hook the reader and establish the high-stakes policy context.
* **Content:**
  * What is the specific question, and why does it matter?
  * What is the "naive" comparison (e.g., OLS or difference-in-means), and why does it suffer from selection bias?
  * Summarize your research design and how it solves the identification problem.
  * Preview the main findings and outline the rest of the paper.

### Section 3: Literature Review & Institutional Background (approx. 1 page)
* **Goal:** Situate your study within existing academic debates and policy contexts.
* **Content:**
  * Review 3–5 key academic papers on the topic. What is the consensus, and what gap does your paper address?
  * Describe the institutional details of the policy, program, or event (e.g., rules of eligibility, timing of implementation, geographical coverage).

### Section 4: Causal Identification Strategy & Theoretical Framework (approx. 1.5 pages)
* **Goal:** Formally defend your research design and identifying assumptions.
* **Content:**
  * **The DAG:** Draw and explain the Directed Acyclic Graph (DAG) representing the causal chain, identifying potential confounders ($X$) and mechanisms.
  * **Formal Model:** Write out your main regression equation using standard econometric notation (e.g., using $\beta$, $\tau_i$, $\alpha_t$). Ensure all subscripts ($i$, $t$) match your data structure.
  * **Identifying Assumptions:** State and defend the core identifying assumptions (e.g., Strict Exogeneity, Common Trends, Conditional Independence, Monotonicity, Exclusion Restriction, Continuity of conditional expectation).
  * **Threats to Validity:** Honestly discuss potential threats (e.g., selection on unobservables, attrition, non-compliance, anticipation, spillover).

### Section 5: Data & Measurement (approx. 1 page)
* **Goal:** Introduce your variables and establish data quality.
* **Content:**
  * Name and describe the data source(s).
  * Clearly define the dependent variable ($Y$), treatment variable ($D$), and key control covariates ($X$).
  * **Table 1: Descriptive Statistics:** Present a clean table showing the mean, standard deviation, minimum, and maximum for your sample, broken down by treatment and control groups if applicable (Balance Table).
  * Discuss missing data, sample restrictions, and tracking of outliers.

### Section 6: Main Results (approx. 2 pages)
* **Goal:** Present your primary empirical findings.
* **Content:**
  * **Table 2: Regression Table:** Present your main econometric results using `stargazer` or `kable` in a multi-column format (e.g., starting with a naive model, adding controls step-by-step, adding fixed effects, or comparing OLS to 2SLS).
  * Interpret the coefficients of interest in prose: specify the units, percentage points, or standard deviations, and discuss statistical significance ($p$-values, standard errors, confidence intervals).
  * **Figure 1: Main Visual:** Include a high-quality visualization (e.g., an event-study plot, RDD discontinuity plot, parallel trends plot, or coefficient plot).

### Section 7: Diagnostics, Robustness, & Falsification Tests (approx. 1.5 pages)
* **Goal:** Prove that your results are not a statistical fluke or driven by model specification choices.
* **Content:**
  * **Falsification/Placebo Tests:** Run a placebo analysis (e.g., placebo treatment dates, placebo outcomes, or testing for pre-trends in event studies).
  * **Robustness Check:** Show that your results hold under alternative specifications (e.g., adding/removing controls, using different functional forms, clustering standard errors at different levels).
  * **Heterogeneity Analysis:** Investigate whether the treatment effect differs across key sub-populations (e.g., by gender, region, or baseline income) using interacted regression models.

### Section 8: Discussion & Policy Implications (approx. 1 page)
* **Goal:** Translate the coefficients back into real-world policy conclusions.
* **Content:**
  * How large is the effect in practical terms? (Compare to standard deviations or baseline means).
  * Conduct a back-of-the-envelope cost-benefit calculation or program scalability analysis.
  * Discuss the generalizability of your findings (external validity).

### Section 9: Conclusion & Appendix (approx. 0.5 pages + Appendix)
* **Goal:** Summarize and hand off.
* **Content:**
  * Brief wrap-up of the main research question and causal findings.
  * Identify 1–2 avenues for future research.
  * **Appendix:** Include fully commented R replication code and any secondary tables/graphs.

---

## 3. Causal Methodology Checklist

Depending on the empirical strategy you select, complete the corresponding checklist below to ensure your quantitative design meets GPEC 446 academic standards.

### 1. Randomized Controlled Trial (RCT) & Covariate Adjustment
* [ ] **Randomization Check:** Verify that treatment assignment ($Z$) is orthogonal to baseline covariates. Run a balance test (joint $F$-test or t-tests across covariates) and present a balance table.
* [ ] **ITT vs. CACE/LATE:** If there is non-compliance, calculate the **Intent-to-Treat (ITT)** effect (OLS of $Y$ on $Z$) and **Complier Average Causal Effect (CACE)** using $Z$ as an instrument for treatment receipt ($D$).
* [ ] **Pre-Treatment Covariates:** Ensure all control variables are strictly measured *pre-treatment*. Never control for post-treatment variables (rules out selection bias / "bad controls").
* [ ] **Freedman's Interacted ANCOVA:** To maximize precision and avoid small-sample bias under heterogeneous treatment effects, demean your covariates ($X_i - \bar{X}$) and interact them with treatment ($D_i$):
  $$Y_i = \beta_0 + \beta_1 D_i + \gamma (X_i - \bar{X}) + \delta D_i (X_i - \bar{X}) + u_i$$
  Verify that the coefficient $\beta_1$ identifies the average treatment effect (ATE).

### 2. OLS with Selection Controls & OVB Diagnosis
* [ ] **Conditional Independence Assumption (CIA):** Explicitly list the unobserved confounders in the error term ($u_i$) and argue why your set of controls ($X_i$) is sufficient to block all back-door paths, satisfying $E[u_i | D_i, X_i] = E[u_i | X_i]$.
* [ ] **Omitted Variable Bias (OVB) Formulations:** For key omitted variables, perform a formal OVB sign and magnitude diagnosis using professor Valasquez's dual notations:
  * **$\pi_1 / \gamma$ Notation:** $\beta_{short} = \beta_{long} + \gamma_{long} \pi_1$ (where $\gamma$ is the effect of the omitted variable on $Y$, and $\pi_1$ is the slope from regressing the omitted variable on $D$).
  * **Covariance/Variance Notation:** $\text{Bias} = c_1 \times c_2$, where $c_1 = \frac{\text{Cov}(Y, W)}{\text{Var}(W)}$ and $c_2 = \frac{\text{Cov}(W, X)}{\text{Var}(X)}$ (where $W$ is the omitted variable).
* [ ] **Bad Control Audit:** Review every control variable and confirm none are post-treatment outcomes that could absorb the treatment effect or open collider bias paths.
* [ ] **Common Support Check:** Ensure there is overlapping covariate distribution (common support) between the treated and untreated groups.

### 3. Instrumental Variables (IV / 2SLS)
* [ ] **First-Stage Strength:** Run the first-stage regression: $D_i = \pi_0 + \pi_1 Z_i + \theta X_i + v_i$.
  * Report the first-stage $F$-statistic on the excluded instrument $Z_i$.
  * Verify that the $F$-statistic exceeds the Staiger-Stock threshold ($F > 10$) or Lee et al. (2022) robust threshold ($F > 104.7$) to rule out weak instrument bias.
* [ ] **Exclusion Restriction:** Provide a strong qualitative, domain-knowledge defense arguing that the instrument $Z_i$ affects the outcome $Y_i$ *only* through its effect on treatment receipt $D_i$. (Recall: this is non-testable).
* [ ] **Independence/Instrument Exogeneity:** Defend why the instrument $Z_i$ is as-good-as-randomly assigned (uncorrelated with the error term $u_i$).
* [ ] **Monotonicity Check:** Argue why there are no "defiers" (units who do the exact opposite of their instrument assignment).
* [ ] **Wald Estimator Walkthrough:** For your baseline model, manually compute the Wald ratio and show that it matches the 2SLS coefficient from `AER::ivreg()`:
  $$\beta_{IV} = \frac{\text{Cov}(Y_i, Z_i)}{\text{Cov}(D_i, Z_i)} = \frac{E[Y_i | Z_i=1] - E[Y_i | Z_i=0]}{E[D_i | Z_i=1] - E[D_i | Z_i=0]}$$

### 4. Differences-in-Differences (DiD) & Two-Way Fixed Effects (TWFE)
* [ ] **Parallel Trends Assumption:** Show that in the pre-treatment period, the treatment and control groups had parallel trajectories.
  * **Event Study:** Run a multi-period event study regression with leads and lags of treatment:
    $$Y_{it} = \alpha_i + \lambda_t + \sum_{k = -M, k \neq -1}^{L} \beta_k D_{it}^k + \varepsilon_{it}$$
    Plot the $\beta_k$ coefficients and verify that all pre-treatment coefficients ($k < -1$) are statistically indistinguishable from zero.
* [ ] **Unit & Time Fixed Effects:** Control for unit fixed effects ($\alpha_i$ to absorb time-invariant unit characteristics) and time fixed effects ($\lambda_t$ to absorb shocks common to all units).
* [ ] **Standard Error Clustering:** Cluster your standard errors at the unit of treatment assignment (e.g., state or school level) to account for serial correlation in errors over time (Bertrand, Duflo, & Mullainathan, 2004).
* [ ] **Staggered Adoption Bias Audit:** If treatment is staggered over time, acknowledge the risk of heterogeneous treatment effects and negative weighting in TWFE (Goodman-Bacon decomposition). If necessary, implement robust estimators such as Callaway & Sant'Anna (2021) or Sun & Abraham (2021) using the `did` package in R.

### 5. Regression Discontinuity Design (RDD)
* [ ] **Running Variable & Cutoff:** Define the running variable ($X_i$) and the sharp or fuzzy cutoff ($c$).
* [ ] **Density Test (McCrary / Cattaneo):** Test for manipulation of the running variable near the cutoff. Run a density test to confirm that units did not systematically sort themselves just above or below the cutoff.
* [ ] **Covariate Continuity:** Verify that pre-treatment covariates are continuous across the cutoff. Present a balance plot showing no jumps in $X$ at $c$.
* [ ] **Bandwidth Selection:** Use optimal bandwidth selection algorithms (e.g., Imbens-Kalyanaraman or Calonico-Cattaneo-Titiunik via `rdrobust` package). Show that your RDD coefficient is robust to using 0.5x and 2x the optimal bandwidth.
* [ ] **Functional Form:** Fit local linear or local quadratic regressions. Avoid high-order polynomials (Gelman & Imbens, 2019).

---

## 4. Diagnostics & Inference Checklist
* [ ] **Serial Correlation (Time-Series / Panels):** If using time series or panel data, check for autocorrelation in the residuals. Run the Durbin-Watson test or Breusch-Godfrey test.
* [ ] **Heteroskedasticity:** Test for heteroskedasticity (Breusch-Pagan or White test). If present, always use robust standard errors (`robust` or `sandwich` in R) or cluster standard errors.
* [ ] **Time-Series Properties (if time series is used):**
  * **Stationarity Test:** Perform an Augmented Dickey-Fuller (ADF) test on your time series variables.
  * **First-Differencing Remedy:** If any series is integrated of order one (I(1)) / highly persistent, first-difference the variables ($\Delta Y_t, \Delta X_t$) before running OLS to prevent spurious regression.
  * **Strict Exogeneity Check (TS.3):** If your time-series model includes lagged dependent variables or feedback loops, do not assume strict exogeneity. Use contemporaneous exogeneity (TS.3') and rely on large-sample OLS asymptotic consistency.
  * **Lags & Seasonality:** Include appropriate lag lengths (AIC/BIC criteria) and seasonal dummy variables to control for periodic patterns.

---

## 5. Course Policy & Academic Integrity Checklist
* [ ] **100% Own-Voice Prose:** Ensure that every explanatory paragraph, literature synthesis, and diagnostic interpretation has been drafted from scratch by you.
* [ ] **Code Verification:** Ensure the R script runs end-to-end without errors. The script must output all tables and figures directly.
* [ ] **Disclosure Block:** Include the standard Course Output Disclosure at the absolute end of the paper, detailing the exact role of any AI tools used in coding or debugging, and verifying that the writing is entirely your own.

---
Generated for: Edgar Agunias
Date: 2026-05-27
Model: Antigravity Orchestrator (durable vector backup restore)
Sources: GPEC 446 Syllabus, Gerber & Green Ch. 4 ANCOVA precision, and Wooldridge Ch. 10-11 Time Series.
Agent: Tyche
---
