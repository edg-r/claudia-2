# GPEC 446 — Running Statistics Concept Notes

A rigorous, exam-aligned statistics glossary and methods cheat sheet for GPEC 446 Quantitative Methods 3.

---

## 1. Core Causal Inference & Potential Outcomes

### Potential Outcomes Framework (Rubin Causal Model)
* **Definition:** For every unit $i$, there are two potential outcomes: $Y_{1i}$ (the outcome if treated, $D_i = 1$) and $Y_{0i}$ (the outcome if untreated, $D_i = 0$).
* **Fundamental Problem of Causal Inference:** We only ever observe the realized outcome $Y_i = D_i Y_{1i} + (1 - D_i) Y_{0i}$. We cannot observe both potential outcomes for the same unit at the same time.
* **Average Treatment Effect (ATE):**
  $$\text{ATE} = E[Y_{1i} - Y_{0i}]$$
* **Average Treatment Effect on the Treated (ATT):**
  $$\text{ATT} = E[Y_{1i} - Y_{0i} | D_i = 1]$$

### Selection Bias
* **Definition:** The difference in average untreated potential outcomes between the treated and untreated groups.
* **Decomposition of Difference in Means:**
  $$\underbrace{E[Y_i | D_i = 1] - E[Y_i | D_i = 0]}_{\text{Observed Difference}} = \underbrace{E[Y_{1i} - Y_{0i} | D_i = 1]}_{\text{ATT}} + \underbrace{E[Y_{0i} | D_i = 1] - E[Y_{0i} | D_i = 0]}_{\text{Selection Bias}}$$
* **Random Assignment Remedy:** Randomization makes treatment assignment $D_i$ independent of potential outcomes: $D_i \perp (Y_{1i}, Y_{0i})$.
  * This guarantees $E[Y_{0i} | D_i = 1] = E[Y_{0i} | D_i = 0]$, eliminating selection bias.
  * Hence, the Observed Difference equals the ATE.

---

## 2. OLS, Selection Controls, & OVB

### Omitted Variable Bias (OVB)
When a variable $W_i$ is omitted from a regression but is correlated with both the treatment $D_i$ and the outcome $Y_i$, OLS estimates of the treatment effect will be biased.

#### Professor Valasquez's Dual Notations for OVB:

1. **$\pi_1 / \gamma$ Parameterization (Structural / Path Form):**
   * **Short Regression:** $Y_i = \alpha_{short} + \beta_{short} D_i + e_i$
   * **Long Regression:** $Y_i = \alpha_{long} + \beta_{long} D_i + \gamma_{long} W_i + u_i$
   * **Auxiliary Regression:** $W_i = \pi_0 + \pi_1 D_i + v_i$
   * **OVB Formula:**
     $$\beta_{short} = \beta_{long} + \underbrace{\gamma_{long} \times \pi_1}_{\text{Bias}}$$
     * *Intuition:* Short coefficient = Long coefficient + (Effect of $W$ on $Y$ $\times$ Relation between $W$ and $D$).

2. **Covariance/Variance Form (Mechanical Form):**
   * Let $W$ be the omitted variable.
   * **OVB Formula:**
     $$\text{Bias} = c_1 \times c_2$$
     where:
     $$c_1 = \frac{\text{Cov}(Y, W)}{\text{Var}(W)} \quad (\text{Effect of omitted variable on outcome } Y)$$
     $$c_2 = \frac{\text{Cov}(W, D)}{\text{Var}(D)} \quad (\text{Relationship between omitted variable and treatment } D)$$

### Conditional Independence Assumption (CIA)
* **Definition:** Also known as Selection on Observables or Unconfoundedness.
* **Formula:** $(Y_{1i}, Y_{0i}) \perp D_i | X_i$
* **Intuition:** Once we control for the set of pre-treatment covariates $X_i$, the treatment assignment is as good as random. Selection bias is eliminated within strata of $X_i$.

### Bad Controls
* **Definition:** Variables that are themselves outcomes of the treatment (post-treatment variables).
* **Trap:** Controlling for post-treatment variables introduces selection bias (collider bias or absorbing the treatment effect) even if treatment was randomly assigned. Controls must be strictly *pre-treatment*.

---

## 3. Instrumental Variables (IV) & LATE

### Wald Estimator
* **Definition:** In a model with a binary instrument $Z_i$ and a binary treatment $D_i$, the IV estimator is the ratio of the reduced form to the first stage:
  $$\beta_{IV} = \frac{\text{Cov}(Y_i, Z_i)}{\text{Cov}(D_i, Z_i)} = \frac{E[Y_i | Z_i=1] - E[Y_i | Z_i=0]}{E[D_i | Z_i=1] - E[D_i | Z_i=0]} = \frac{\text{Reduced Form}}{\text{First Stage}}$$

### Four Identifying Assumptions for LATE (AIR, 1996):
1. **Instrument Random Assignment (Independence):** $Z_i$ is as-good-as-randomly assigned, uncorrelated with potential outcomes and compliance types.
2. **First Stage (Relevance):** The instrument affects treatment take-up: $E[D_i | Z_i=1] - E[D_i | Z_i=0] \neq 0$. Tested via first-stage regression $F$-statistic (threshold $F > 10$ or $F > 104.7$).
3. **Exclusion Restriction:** The instrument affects the outcome $Y_i$ *only* through its effect on treatment take-up $D_i$. Formally: $Y_i(d, z) = Y_i(d)$.
4. **Monotonicity:** There are no "defiers" (no units who do the exact opposite of their instrument assignment). Formally: $D_{1i} \geq D_{0i}$ for all $i$.

### Compliance Types & Local Average Causal Effect (LATE)
Monotonicity classifies the population into three active compliance groups:
* **Compliers ($D_{1i}=1, D_{0i}=0$):** Take treatment if assigned, do not if not assigned.
* **Always-Takers ($D_{1i}=1, D_{0i}=1$):** Take treatment regardless of assignment.
* **Never-Takers ($D_{1i}=0, D_{0i}=0$):** Never take treatment regardless of assignment.
* **Defiers ($D_{1i}=0, D_{0i}=1$):** Do the opposite of assignment (ruled out by monotonicity).

* **LATE / CACE Theorem:** The IV estimator identifies the average treatment effect *specifically for the compliers*:
  $$\beta_{IV} = E[Y_{1i} - Y_{0i} | \text{Compliers}]$$
  * *Trap:* IV does not identify the ATE for Always-Takers or Never-Takers, as the instrument does not shift their treatment status.

---

## 4. Panel Data & Difference-in-Differences (DiD)

### Two-Period Difference-in-Differences (DiD)
* **Definition:** Compares the change in outcomes over time between a treated group and a control group.
* **Empirical Regression:**
  $$Y_{it} = \beta_0 + \beta_1 \text{Treated}_i + \beta_2 \text{Post}_t + \delta (\text{Treated}_i \times \text{Post}_t) + \varepsilon_{it}$$
  * $\delta$ is the DiD estimator, capturing the causal effect.
* **Parallel Trends Assumption:** In the absence of treatment, the average outcomes for the treated and control groups would have followed parallel paths over time.
  $$E[Y_{0i, \text{Post}} - Y_{0i, \text{Pre}} | \text{Treated}] = E[Y_{0i, \text{Post}} - Y_{0i, \text{Pre}} | \text{Control}]$$

### Two-Way Fixed Effects (TWFE) & Event Studies
* **TWFE Model:** Extends DiD to multiple periods and units:
  $$Y_{it} = \alpha_i + \lambda_t + \beta D_{it} + \varepsilon_{it}$$
  where $\alpha_i$ are unit fixed effects (absorb all time-invariant confounders) and $\lambda_t$ are time fixed effects (absorb shocks common to all units).
* **Event Study Model:** Allows testing for pre-trends and dynamic effects:
  $$Y_{it} = \alpha_i + \lambda_t + \sum_{k = -M, k \neq -1}^{L} \beta_k D_{it}^k + \varepsilon_{it}$$
  * *Identification Test:* Parallel trends are plausible if pre-treatment coefficients ($\beta_k$ for $k < -1$) are close to zero and statistically insignificant.
* **Goodman-Bacon Decomposition & Staggered Adoption Bias:**
  * Under staggered treatment timing, TWFE is a weighted average of all possible two-group/two-period DiD comparisons.
  * *Trap:* Early-treated units act as controls for late-treated units. If treatment effects vary over time, this can lead to negative weights and severely biased estimators. Solution: use robust estimators (e.g., Callaway & Sant'Anna).

---

## 5. Regression Discontinuity Design (RDD)

### RDD Identification Logic
* **Definition:** Assignment to treatment is determined by whether a continuous running variable $X_i$ falls above or below a strict threshold $c$: $D_i = 1[X_i \geq c]$.
* **Identifying Assumption (Continuity):** The conditional expectations of potential outcomes $E[Y_{1i}|X_i]$ and $E[Y_{0i}|X_i]$ are continuous functions of $X_i$ at the cutoff $c$.
* **Sharp vs. Fuzzy RDD:**
  * **Sharp RDD:** Probability of treatment jumps from 0 to 1 at the cutoff:
    $$\lim_{x \downarrow c} P(D_i=1|X_i=x) - \lim_{x \uparrow c} P(D_i=1|X_i=x) = 1$$
  * **Fuzzy RDD:** Take-up jumps discontinuously at the cutoff but is not 0/1 (acts as an instrument):
    $$\lim_{x \downarrow c} P(D_i=1|X_i=x) - \lim_{x \uparrow c} P(D_i=1|X_i=x) < 1$$
    Identified via Wald-style RDD:
    $$\beta_{Fuzzy} = \frac{\lim_{x \downarrow c} E[Y_i|X_i=x] - \lim_{x \uparrow c} E[Y_i|X_i=x]}{\lim_{x \downarrow c} E[D_i|X_i=x] - \lim_{x \uparrow c} E[D_i|X_i=x]}$$

* **McCrary / Cattaneo Density Test:** Tests for sorting behavior. If units can manipulate their running variable to place themselves on one side of the cutoff, there will be a discontinuity in the density of $X_i$ at $c$, violating the design.

---

## 6. Covariate Adjustment in Randomized Experiments
*(Gerber & Green Ch. 4)*

### Prognostic Covariates
* **Definition:** Baseline variables ($X_i$) that are highly correlated with the potential outcomes $(Y_{1i}, Y_{0i})$ but are measured pre-treatment.
* **Precision and Efficiency:** Since treatment is randomized, adjusting for covariates is *never* required for unbiasedness. However, doing so reduces the residual variance ($\sigma^2_u$), which shrinks standard errors and increases statistical power.

### Freedman's Critique & Interacted ANCOVA
* **The Critique (Freedman, 2008):** In small samples with heterogeneous treatment effects, simple OLS adjustment ($Y_i = \beta_0 + \beta_1 D_i + \gamma X_i + e_i$) can actually *increase* standard errors or introduce small-sample bias.
* **The Solution:** Demean your covariates ($X_i - \bar{X}$) and interact them with the treatment indicator:
  $$Y_i = \beta_0 + \beta_1 D_i + \gamma (X_i - \bar{X}) + \delta D_i (X_i - \bar{X}) + \varepsilon_i$$
  This interacted ANCOVA specification guarantees that $\beta_1$ remains a consistent, asymptotically efficient, and unbiased estimator of the Average Treatment Effect (ATE) even under heterogeneous treatment effects.

---

## 7. Time Series OLS Estimation
*(Wooldridge Ch. 10–11)*

### Finite Distributed Lag (FDL) Model
* **Definition:** A model that includes lags of the independent variable to capture dynamic adjustments over time.
  $$Y_t = \alpha_0 + \delta_0 Z_t + \delta_1 Z_{t-1} + \delta_2 Z_{t-2} + \dots + \delta_q Z_{t-q} + u_t$$
* **Impact Propensity (Short-Run Effect):** $\delta_0$, the immediate effect of a temporary one-unit change in $Z_t$ on $Y_t$.
* **Long-Run Propensity (LRP):** The total long-run change in $Y_t$ given a permanent, one-unit increase in $Z_t$:
  $$\text{LRP} = \sum_{j=0}^{q} \delta_j$$

### Strict Exogeneity vs. Contemporaneous Exogeneity
* **Strict Exogeneity (TS.3):**
  $$E[u_t | \mathbf{Z}] = 0 \quad \text{for all } t$$
  * **Meaning:** The error at time $t$ is uncorrelated with the independent variables in *every* period (past, present, future).
  * **Violations:** Lagged dependent variables (e.g., $Y_{t-1}$ as a regressor) or feedback loops (where shocks to $Y_t$ affect future values of $Z$) violate strict exogeneity.
  * **Use:** Required for finite-sample unbiasedness of OLS.

* **Contemporaneous Exogeneity (TS.3'):**
  $$E[u_t | \mathbf{z}_t] = 0 \quad \text{for all } t$$
  * **Meaning:** The error at time $t$ is uncorrelated only with the regressors in the *same* period.
  * **Use:** Much weaker than strict exogeneity. Allows lagged dependent variables and feedback loops. Sufficient for asymptotic consistency under OLS.

### Covariance Stationarity & Weak Dependence
* **Covariance Stationary Process:** A stochastic process $\{X_t\}$ is covariance stationary if:
  1. $E[X_t] = \mu$ (constant mean over time).
  2. $Var(X_t) = \sigma^2$ (constant variance over time).
  3. $Cov(X_t, X_{t+h}) = \gamma_h$ (covariance depends only on the lag $h$, not on $t$).
* **Weakly Dependent Process:** A stationary process is weakly dependent if the correlation between $X_t$ and $X_{t+h}$ goes to 0 as $h \to \infty$. This ensures that the Law of Large Numbers (LLN) and Central Limit Theorem (CLT) apply to time series.
  * *Example:* An AR(1) process $Y_t = \rho Y_{t-1} + e_t$ is stationary and weakly dependent if and only if $|\rho| < 1$.

### Unit Roots & Spurious Regressions
* **Unit Root / Random Walk (Highly Persistent):**
  $$Y_t = Y_{t-1} + e_t \quad (\text{where } \rho=1)$$
  * **Properties:** Highly non-stationary. The variance of $Y_t$ is $\sigma^2 t$, which grows with time. Violates weak dependence.
* **Spurious Regression:** If you regress one independent unit-root process on another, OLS will yield highly significant coefficients, very low $p$-values, and a high $R^2$, which are completely spurious and misleading.
* **First-Differencing Remedy:** If a process is $I(1)$ (has a unit root), first-differencing it creates a stationary $I(0)$ process:
  $$\Delta Y_t = Y_t - Y_{t-1} = e_t$$
  This allows OLS to yield valid consistent estimates.

---
Generated for: Edgar Agunias
Date: 2026-05-27
Model: Claude 3.5 Sonnet (subagent execution)
Sources: GPEC 446 Syllabus, syllabus_extracted.md, Gerber & Green Ch. 4 (Using Covariates to Rescale Outcomes) concepts, and Wooldridge Ch. 10-11 (Time Series Basics and Asymptotics) concepts.
Agent: Tyche
---

