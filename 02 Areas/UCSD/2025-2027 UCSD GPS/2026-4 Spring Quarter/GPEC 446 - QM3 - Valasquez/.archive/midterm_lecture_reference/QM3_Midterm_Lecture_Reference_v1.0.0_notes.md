# QM3 Midterm Lecture Reference v1.0.0

This reference sheet is built from the QM3 lecture slides, not the textbook-centered methods guide. Use it as an exam-facing checklist: identify the method, name the identifying assumption, say what comparison is being made, then interpret the estimate in the units of the outcome.

## Source Map

| Lecture | Slides | Core midterm use |
|---|---|---|
| L1 | `QM3_L1_Intro.pdf` | Causal inference as policy evaluation; correlation vs causation; counterfactual logic; research design over pure math. |
| L2 | `QM3_L2_CaInf.pdf` | Potential outcomes; ATE/ATT; naive comparisons; selection bias; random assignment as the solution. |
| L3 | `QM3_L3_Reg.pdf` | OLS mechanics; coefficients; dummies; interactions; regression as stratification; CIA/common support. |
| L4 | `QM3_L4_Reg2.pdf` | OLS treatment effects; endogeneity; OVB formula; simultaneity; measurement error and attenuation bias. |
| L5 | `QM3_L5_IV.pdf` | Bad controls; IV notation; first stage, reduced form, exclusion; weak instruments; 2SLS. |
| L6 | `QM3_L6_IV2.pdf` | IV as potential outcomes; compliance types; ITT/TOT/LATE; AIR assumptions; PACES voucher example. |

## The Exam Algorithm

1. **Name the estimand.** ATE, ATT/TOT, ITT, or LATE.
2. **Name the comparison.** Difference in means, regression-adjusted comparison, first stage, reduced form, Wald/2SLS.
3. **State the identifying assumption.** Random assignment, CIA plus common support, exogeneity, exclusion restriction, monotonicity, or no measurement error.
4. **State the failure mode.** Selection, bad controls, OVB, simultaneity, measurement error, weak instrument, exclusion violation.
5. **Interpret in units.** Dollars, years, percentage points, test-score points, etc. Do not say "percent" when the slide quantity is a difference in rates.

## 1. Causal Inference and Identification

**Lecture source:** L1 "What Is This Class About?" and "Pearl and the Ladder of Causation"; L2 "What do we mean by identification?"

**Concept:** QM3 is about estimating causal policy impacts from real-world data. The key lecture distinction is that observed patterns live at the correlation/observation level, while causal inference requires an intervention or a credible counterfactual. Identification asks whether the desired causal quantity can be recovered from the available data plus assumptions; more observations alone do not fix an unidentified design.

**When/how to use it:** Start any short answer by separating the policy question from the data pattern. For example: "The observed employment gap is a correlation; to call it causal, we need an identification strategy explaining why treatment status is unrelated to the potential outcomes."

**Formula/notation:** Identification strategy = source of identifying variation + method used to exploit it. The method can be difference in means, OLS, IV, or 2SLS, but the source of variation is the causal core.

**Interpretation traps:** A regression coefficient is not automatically causal. A large sample reduces sampling uncertainty but does not remove selection bias. A "program works" claim needs an impact-evaluation counterfactual, not only evidence that participants improved.

**Exam cues:** Prompts that ask "what assumptions are behind this conclusion?", "how should we interpret this average difference?", or "what makes this comparison causal?" are identification questions before they are calculation questions.

## 2. Potential Outcomes, ATE, ATT, and Selection

**Lecture source:** L2 "Identification in the potential outcomes model," "Treatment Parameters," "The Naive Estimator vs the ATE," and "Selection and ATT."

**Concept:** Each unit has two potential outcomes, `Y_i(1)` under treatment and `Y_i(0)` without treatment, but only one is observed. The individual causal effect is `tau_i = Y_i(1) - Y_i(0)`. The ATE averages this over the population; ATT averages it over treated units. The naive treated-control difference mixes the causal effect with selection.

**When/how to use it:** Use potential-outcomes language whenever a prompt gives treated and untreated groups and asks whether a raw difference is causal. Ask which missing counterfactual is being substituted by the comparison group.

**Formula/notation:**

```text
Observed outcome: Y_i = D_i * Y_i(1) + (1 - D_i) * Y_i(0)
ATE = E[Y_i(1) - Y_i(0)]
ATT = E[Y_i(1) - Y_i(0) | D_i = 1]
Difference in means = ATT + {E[Y_i(0)|D_i=1] - E[Y_i(0)|D_i=0]}
```

**Interpretation traps:** The observed control group mean is not automatically the treated group's missing untreated mean. If treated units selected into treatment because they expected higher gains or had worse baseline conditions, the selection term can be positive or negative.

**Exam cues:** If a prompt says "participants did worse than nonparticipants," do not conclude treatment harmed them until you discuss selection. The Maria/Khuzdar example in L2 is the clean lecture cue: the observed comparison can have the opposite sign from the individual treatment effect.

## 3. Random Assignment

**Lecture source:** L2 "Identification under random assignment" and "Random Assignment as solution"; L3 "No Random Assignment."

**Concept:** Random assignment solves selection because treatment status is independent of potential outcomes. Treated and control groups come from the same population, so their expected untreated outcomes are equal. Then the difference in means identifies the causal effect in expectation.

**When/how to use it:** Use this for randomized programs, lotteries, or experiments. Explain that randomization balances observed and unobserved characteristics on average. If the sample is random, the law of large numbers makes the sample resemble the population.

**Formula/notation:**

```text
D_i independent of (Y_i(1), Y_i(0)), with 0 < Pr(D_i = 1) < 1
E[Y_i(0)|D_i=1] - E[Y_i(0)|D_i=0] = 0
Under random assignment: E[Y|D=1] - E[Y|D=0] = ATE
```

**Interpretation traps:** Random assignment is about the assignment mechanism, not about whether groups look perfectly identical in a finite sample. Also distinguish assignment from take-up: if compliance is incomplete, a randomized assignment contrast is an ITT unless scaled by compliance under extra assumptions.

**Exam cues:** Words like "lottery," "randomly assigned," "same population," "balanced," or "observables and unobservables" point to this section.

## 4. OLS and Regression Interpretation

**Lecture source:** L3 "OLS," "OLS as Minimizing Residuals," "Interpreting OLS Coefficients," and L4 "Using OLS to Estimate Treatment Effects."

**Concept:** OLS finds the line that minimizes squared residuals. A simple slope is `Cov(X,Y)/Var(X)`. In multiple regression, each coefficient is a conditional association: the predicted change in `Y` for a one-unit increase in that predictor, holding included predictors fixed. It becomes causal only when the treatment variable is unrelated to the error term after the model's controls.

**When/how to use it:** Use OLS for coefficient interpretation, regression tables, and questions that ask what a control changes. State the outcome units, the regressor units, and exactly which included variables are held fixed.

**Formula/notation:**

```text
Fitted value: Yhat_i = beta_hat_0 + beta_hat_1 X_i
Residual: uhat_i = Y_i - Yhat_i
Simple OLS slope: beta_hat_1 = Cov(X,Y) / Var(X)
Multiple regression: Y_i = beta_0 + beta_1 D_i + beta_2 X_i + epsilon_i
Key causal condition: E(epsilon_i | D_i, X_i) = 0
```

**Interpretation traps:** "Holding all else constant" only means holding included right-hand-side variables constant. If an important confounder is omitted, the coefficient is still biased. If a variable is post-treatment, adding it can make the estimate worse.

**Exam cues:** Regression-output questions usually want the coefficient interpretation first and the causal assumption second. If the prompt asks whether OLS "recovers" the effect, answer with `E(epsilon_i | D_i, X_i) = 0` or the equivalent ceteris-paribus/random-assignment statement.

## 5. Dummies, Interactions, and Demeaning

**Lecture source:** L3 "Binary Variables on the Right-Hand Side," "Dummy Variables - Other Uses," "Interactions Between Dummy Variables," and "Interactions: Continuous Variables and Demeaning."

**Concept:** Dummy variables turn categories into regression comparisons against an omitted/reference category. Interactions let effects differ across groups or levels of another variable. With dummy-by-dummy interactions, the interaction coefficient is the extra joint effect beyond the two main effects. With continuous-by-dummy interactions, the dummy main effect is evaluated when the continuous variable equals zero unless the continuous variable is demeaned.

**When/how to use it:** Use this when reading regression tables with `factor(...)`, group dummies, or terms like `female * asian` or `IQ * female`. Add coefficients to get group-specific effects.

**Formula/notation:**

```text
Dummy interaction:
earnings_i = b0 + b1 female_i + b2 asian_i + b3(asian_i*female_i) + e_i
b1 = female gap for non-Asian workers
b2 = Asian male gap relative to non-Asian men
b3 = extra Asian-woman difference

Demeaning:
IQ_tilde_i = IQ_i - mean(IQ)
Then b1 is the female gap at average IQ
```

**Interpretation traps:** Do not interpret the interaction coefficient as the full effect for the interacted group. Do not interpret a main effect without checking the reference category and the zero point of continuous variables.

**Exam cues:** Prompts asking "what is the effect for group X?" usually require adding a main coefficient and an interaction coefficient. Prompts asking why demeaning helps are about making the main dummy effect meaningful at an average baseline.

## 6. Selection on Observables, CIA, and Common Support

**Lecture source:** L3 "Selection on Observables," "Formal Identification Assumptions," and "CIA Interpretation."

**Concept:** When randomization is not feasible, regression can approximate stratification by comparing treated and control units with the same observed characteristics. The Conditional Independence Assumption says treatment is as good as randomly assigned after conditioning on `X_i`. Common support says that for each relevant value of `X_i`, both treated and untreated units exist.

**When/how to use it:** Use this for observational studies with controls. Make the credibility argument: why would two units identical on meaningful background factors still receive different treatment?

**Formula/notation:**

```text
CIA: (Y_i(1), Y_i(0)) independent of D_i conditional on X_i
Common support: 0 < Pr(D_i = 1 | X_i) < 1
```

**Interpretation traps:** Controls only adjust for observed covariates. If unobserved motivation, ability, family background, location, or networks still affect both treatment and outcome, CIA fails. No overlap means regression extrapolates rather than compares like with like.

**Exam cues:** "Compare people who applied to the same colleges but chose differently" is the lecture's private-university cue for selection on observables. "For every value of X, we need both treated and untreated units" is common support.

## 7. Omitted Variable Bias

**Lecture source:** L4 "All Else Constant?" and "OVB: The Formula."

**Concept:** OVB occurs when an omitted confounder affects the outcome and is correlated with the treatment/regressor. The short regression wrongly attributes the omitted variable's effect to the included variable. In the private-university example, higher-earning applicant groups are also more likely to attend private schools, so the raw private-school coefficient is upward biased.

**When/how to use it:** Use this whenever a prompt asks for the direction of bias or gives a short and long regression. Sign the two pieces separately: omitted variable to treatment, and omitted variable to outcome.

**Formula/notation:**

```text
Long regression:  Y_i = alpha_l + beta_l P_i + gamma A_i + epsilon_li
Short regression: Y_i = alpha_s + beta_s P_i + epsilon_si
Auxiliary regression: A_i = pi_0 + pi_1 P_i + u_i
OVB = beta_s - beta_l = pi_1 * gamma
```

**Interpretation traps:** No bias if either `pi_1 = 0` or `gamma = 0`. Positive correlation plus positive omitted-variable effect gives positive bias; opposite signs give negative bias. The true effect is the short coefficient minus the bias.

**Exam cues:** Phrases like "ability," "family background," "selection controls," "short versus long regression," or "what is the direction of bias?" point here.

## 8. Simultaneity and Measurement Error

**Lecture source:** L4 "Simultaneity," "Simultaneity Bias: The Formal Problem," and "Measurement Error: Attenuation Bias."

**Concept:** Simultaneity means the explanatory variable and outcome are co-determined, so the regressor is correlated with the error term. The police/crime example is the lecture anchor: crime affects police deployment, and police affect crime. Measurement error means the regressor is observed with noise; classical measurement error attenuates the coefficient toward zero.

**When/how to use it:** Use simultaneity when the causal arrow plausibly runs both ways. Use measurement error when the variable of interest is survey-reported, mismeasured, or proxied.

**Formula/notation:**

```text
Endogeneity: E(epsilon_i | X_i) != 0

Simultaneity example:
Y_1 = alpha_1 Y_2 + beta_1 Z_1 + mu_1
Y_2 = alpha_2 Y_1 + beta_2 Z_2 + mu_2

Classical measurement error:
S_i = S_i* + m_i
beta_hat_bad = r * beta, where
r = Var(S_i*) / [Var(S_i*) + Var(m_i)], and 0 < r < 1
```

**Interpretation traps:** Adding ordinary controls may not solve simultaneity because the problem is feedback, not only missing covariates. With measurement error, a small coefficient may understate a larger true effect because noise has pushed the estimate toward zero.

**Exam cues:** "More police are deployed to high-crime areas" is simultaneity. "Self-reported income," "conflict event counts," or "mismeasured schooling" are measurement-error cues.

## 9. Bad Controls and Post-Treatment Bias

**Lecture source:** L5 "Bad Controls" and "Post-treatment bias: Example."

**Concept:** More controls are not always better. Bad controls are variables that are themselves outcome variables in the notional experiment, especially post-treatment variables. Controlling for a mediator blocks part of the treatment effect and changes the estimand.

**When/how to use it:** Use this when a proposed control is caused by treatment. In the job-training example, employment one year later is part of the pathway from training to annual income. Controlling for employment asks a different question: whether training raises income among people with the same employment outcome.

**Formula/notation:**

```text
Treatment: Z
Mediator/post-treatment variable: S = Z + error_S
Outcome: Y = Z + S + error_Y
Total effect of Z on Y includes the direct path plus the indirect path through S.
Controlling for S blocks the indirect path.
```

**Interpretation traps:** A variable can be predictive and still be a bad control. The question is temporal and causal: was it determined before treatment, or is it itself affected by treatment?

**Exam cues:** "Should we control for employment after job training?", "control for income after education," or "post-treatment variable" points here. The right answer is usually to describe how the control steals away part of the effect.

## 10. Instrumental Variables and 2SLS

**Lecture source:** L5 "Instrumental Variables," "Identification," "Bias and Weak Instruments," "IV Estimation," and "Remarks."

**Concept:** IV uses an external source of variation `Z` that affects the endogenous regressor `X` but affects the outcome `Y` only through `X`. The first stage is `Z -> X`; the reduced form is `Z -> Y`; the exclusion restriction says there is no direct `Z -> Y` path except through `X`.

**When/how to use it:** Use IV when OLS is threatened by OVB, measurement error, or simultaneity. The rainfall/GDP/conflict example is the L5 anchor: rainfall shifts GDP growth, and the design argues rainfall does not directly respond to conflict.

**Formula/notation:**

```text
Structural equation: Y_i = alpha + rho X_i + eta_i
First stage: X_i = pi_0 + pi_1 Z_i + u_i
IV/Wald estimand: rho = Cov(Y_i, Z_i) / Cov(X_i, Z_i)
Equivalent binary form: Reduced Form / First Stage

2SLS:
1st stage: X_i = pi_0 + pi_1 Z_i + u_i, get Xhat_i
2nd stage: Y_i = alpha + rho Xhat_i + v_i
R pattern: ivreg(Y ~ X1 + X2 | Z + X2, data = dat)
```

**Interpretation traps:** The first stage can be checked; exclusion cannot be directly tested. Weak instruments make the denominator small and estimates volatile. If the instrument is imperfect, weak first stage can amplify the bias. L5 notes old-school `F > 10` and newer `F > 104.7` thresholds.

**Exam cues:** "Instrument validity" means state first stage and exclusion. "Weak instrument" means small `Cov(X,Z)`, low first-stage strength, volatile estimates, and possible bias amplification.

## 11. ITT, TOT, Compliance Types, and LATE

**Lecture source:** L6 "IV, Assignment and Take-up," "Estimations," "Estimation - One-sided compliance," "Estimation - Two-sided compliance," "Identification," and "Identification: LATE."

**Concept:** In real programs, assignment and treatment take-up differ. ITT is the effect of being assigned or offered treatment. TOT/ATT is the effect on those who actually receive treatment. LATE is the treatment effect for compliers, the subgroup whose treatment status is changed by the assignment or instrument.

**When/how to use it:** Use this for lotteries, vouchers, scholarships, and any program with incomplete take-up. In PACES, lottery assignment created the opportunity to attend private school, but not everyone complied, and some non-winners still received scholarships.

**Formula/notation:**

```text
Compliance types:
Always-takers: (D1, D0) = (1, 1)
Never-takers:  (D1, D0) = (0, 0)
Compliers:     (D1, D0) = (1, 0)
Defiers:       (D1, D0) = (0, 1)

One-sided compliance:
TOT = ITT / compliance

Two-sided compliance / LATE:
LATE = [E(Y|Z=1) - E(Y|Z=0)] / [E(D|Z=1) - E(D|Z=0)]
     = Reduced Form / First Stage
```

**Interpretation traps:** ITT can be the policy-relevant estimand if the decision is whether to offer a program. LATE is not the ATE; it applies to compliers. Always-takers and never-takers do not identify the treatment effect because assignment does not change their treatment status. Monotonicity rules out defiers.

**Exam cues:** "Lottery winners were X percentage points more likely to take treatment" gives the first stage. "What share are always-takers, never-takers, and compliers?" means use observed take-up among `Z=0` and `Z=1`: with monotonicity, `p_A = Pr(D=1|Z=0)`, `p_N = Pr(D=0|Z=1)`, and `p_C = Pr(D=1|Z=1) - Pr(D=1|Z=0)`.

## 12. IV Identification Assumptions Under Potential Outcomes

**Lecture source:** L6 "Identification (Angrist et al. 1996)" and "Identification: LATE."

**Concept:** L6 translates IV into the potential-outcomes framework. The AIR assumptions are: random assignment of `Z`, a nonzero first stage, exclusion restriction, and monotonicity. Under these assumptions, the Wald ratio identifies the complier average effect.

**When/how to use it:** Use this when an IV question asks for validity conditions or what IV identifies. List the assumptions, then say which are testable.

**Formula/notation:**

```text
Random assignment:
({Y_i(d,z) for all d,z}, D_1i, D_0i) independent of Z_i

First stage:
E[D_i|Z_i=1] - E[D_i|Z_i=0] != 0

Exclusion:
Y_i(d,0) = Y_i(d,1) = Y_di for d = 0,1

Monotonicity:
D_1i - D_0i >= 0 for all i

LATE theorem:
rho_C = [E(Y|Z=1) - E(Y|Z=0)] / [E(D|Z=1) - E(D|Z=0)]
```

**Interpretation traps:** Random assignment of `Z` is not the same as random assignment of treatment `D`. Exclusion is usually the key vulnerability. Placebo tests can support the story but do not prove exclusion.

**Exam cues:** "What is the exclusion restriction saying?" is the professor's IV validity cue. Answer in words tied to the case: "the lottery affects test scores only by changing private-school attendance," not merely "Z only affects Y through X."

## Final One-Page Memory Check

- **Potential outcomes:** Always ask what counterfactual is missing.
- **Random assignment:** Difference in means identifies causal effect because selection bias is zero in expectation.
- **OLS:** Coefficients are conditional associations unless the error is unrelated to the regressor after controls.
- **CIA/common support:** Treated and control units must be comparable within observed covariate cells.
- **OVB:** Bias equals omitted-treatment relationship times omitted-outcome effect.
- **Simultaneity:** Feedback makes the regressor endogenous.
- **Measurement error:** Classical noise in `X` attenuates the coefficient toward zero.
- **Bad controls:** Do not control for variables caused by treatment unless you intentionally want a mediated/direct-effect estimand.
- **IV:** Validity requires first stage plus exclusion; weak first stage makes IV volatile and potentially more biased if exclusion is imperfect.
- **LATE:** IV with noncompliance estimates the effect for compliers, not everyone.

---
Generated for: Edgar Agunias
Date: 2026-04-30
Model: GPT-5 (Codex, reasoning effort not exposed)
Sources: QM3 lecture slides L1-L6 (`QM3_L1_Intro.pdf`, `QM3_L2_CaInf.pdf`, `QM3_L3_Reg.pdf`, `QM3_L4_Reg2.pdf`, `QM3_L5_IV.pdf`, `QM3_L6_IV2.pdf`); Tyche memory files; existing QM3 midterm methods reference used for style/format only
Agent: Tyche
---
