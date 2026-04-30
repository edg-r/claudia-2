# Quantitative Methods 3 (QM3) Midterm Lecture Reference v1.2.1

This reference sheet is built from the QM3 lecture slides, not the textbook-centered methods guide. The v1.2.1 patch preserves v1.2.0's narrative exam-facing approach and visual aids, then fixes formula-block wrapping, expands acronyms on first use, and adds a short "Explain Like I'm 5" conclusion to each numbered topic.

## Source Map

| Lecture | Slides | Core midterm use |
|---|---|---|
| Lecture 1 (L1) | `QM3_L1_Intro.pdf` | Causal inference as policy evaluation; correlation versus causation; counterfactual logic; research design over pure math. |
| Lecture 2 (L2) | `QM3_L2_CaInf.pdf` | Potential outcomes; Average Treatment Effect (ATE); Average Treatment effect on the Treated (ATT); naive comparisons; selection bias; random assignment as the solution. |
| Lecture 3 (L3) | `QM3_L3_Reg.pdf` | Ordinary Least Squares (OLS) mechanics; coefficients; dummy variables; interactions; regression as stratification; Conditional Independence Assumption (CIA); common support. |
| Lecture 4 (L4) | `QM3_L4_Reg2.pdf` | OLS treatment effects; endogeneity; Omitted Variable Bias (OVB); simultaneity; measurement error and attenuation bias. |
| Lecture 5 (L5) | `QM3_L5_IV.pdf` | Bad controls; Instrumental Variables (IV) notation; first stage; reduced form; exclusion restriction; weak instruments; Two-Stage Least Squares (2SLS). |
| Lecture 6 (L6) | `QM3_L6_IV2.pdf` | IV as potential outcomes; compliance types; Intention-to-Treat (ITT); Treatment-on-the-Treated (TOT); Local Average Treatment Effect (LATE); Angrist-Imbens-Rubin (AIR) assumptions; Programa de Ampliacion de Cobertura de la Educacion Secundaria (PACES) voucher example. |

## The Exam Algorithm

1. **Name the causal object.** Decide whether the prompt wants ATE, ATT/TOT, ITT, or LATE. This usually determines the rest of the answer.
2. **Name the comparison.** Say whether the estimate is a raw treated-control difference, a regression-adjusted comparison, a first stage, a reduced form, a Wald ratio, or 2SLS.
3. **Name the identifying assumption.** The answer is not causal until you say why the comparison substitutes for the missing counterfactual: random assignment, Conditional Independence Assumption (CIA) plus common support, exogeneity, exclusion restriction, monotonicity, or accurate measurement.
4. **Name the failure mode.** If the assumption is not credible, label the problem: selection, bad control, OVB, simultaneity, measurement error, weak instrument, or exclusion violation.
5. **Interpret in units.** State the outcome units and direction. A 0.11 change in a rate is 11 percentage points, not 11 percent.

## 1. Causal Inference and Identification

**Core idea:** QM3 treats causal inference as a design problem before it is a calculation problem. A policy question asks what would happen if a unit received treatment instead of not receiving it. The data only show one realized world, so the whole task is to defend a comparison group that stands in for the missing counterfactual. Identification means the causal quantity can be recovered from the observed data under a stated set of assumptions.

**How to recognize it on the exam:** If the prompt asks whether a comparison is "causal," whether a conclusion is "identified," or what makes a research design credible, start here. The key move is to separate the observed pattern from the causal claim. "Participants earn more than nonparticipants" is a descriptive comparison; "the program raised earnings" requires an identification story.

**Comparison being made:** Any method in the course is a way of making a counterfactual comparison. Randomized difference in means compares assigned treatment and control groups. OLS compares units after conditioning on included variables. IV compares outcome changes induced by an instrument. The method is only the calculation; the identifying variation is the reason the calculation is meaningful.

**Identifying assumption:** The comparison group must represent what treated units would have looked like without treatment, or what untreated units would have looked like with treatment. More observations reduce noise around a bad comparison; they do not make the comparison causal.

**Formula/notation:**

```text
Identification strategy = source of identifying variation + method that exploits it
Causal claim = observed comparison + assumption that supplies the missing counterfactual
```

**Visual aid:** The first diagram shows the core counterfactual problem: for the same unit, one potential outcome is observed and the other is missing.

[[VISUAL:potential_outcomes]]

**Interpretation sentence:** "This estimate can be interpreted causally only if the design makes treatment status unrelated to the potential outcome that is missing for each unit."

**Common trap:** Do not say a coefficient is causal because it is statistically significant, large, or estimated on a big dataset. Significance is about sampling uncertainty; identification is about bias.

**Explain Like I'm 5:** A causal claim is not just noticing two things move together. It is showing that your comparison group is a believable stand-in for the missing "what would have happened otherwise" world.

## 2. Potential Outcomes, ATE, ATT, and Selection

**Core idea:** Potential outcomes force the counterfactual problem into notation. Each unit has `Y_i(1)` if treated and `Y_i(0)` if untreated, but we observe only one of them. A causal effect is the difference between those two potential outcomes for the same unit. Since the missing potential outcome is never observed directly, group comparisons can mix treatment effects with pre-existing differences between treated and untreated units.

**How to recognize it on the exam:** Use this section whenever a prompt gives treated and untreated groups and asks whether the raw difference is a treatment effect. The exam cue is usually a substantive contrast: program participants versus nonparticipants, private college attendees versus public college attendees, or households in a treated area versus others.

**Comparison being made:** The naive comparison is `E[Y_i | D_i = 1] - E[Y_i | D_i = 0]`. It compares observed treated outcomes for treated units to observed untreated outcomes for untreated units. That is not the same as comparing treated units to themselves under no treatment.

**Identifying assumption:** To read the naive comparison as causal, the untreated potential outcome for treated units must equal the untreated outcome for controls in expectation. If treated units selected into treatment because they were richer, poorer, more motivated, or more exposed to the policy, that equality fails.

**Formula/notation:**

```text
Observed outcome:
Y_i = D_i * Y_i(1) + (1 - D_i) * Y_i(0)

ATE = E[Y_i(1) - Y_i(0)]
ATT = E[Y_i(1) - Y_i(0) | D_i = 1]

Difference in means =
ATT + {E[Y_i(0) | D_i = 1] - E[Y_i(0) | D_i = 0]}
```

**Interpretation sentence:** "The raw treated-control gap equals the treatment effect for treated units plus a selection term, so it is causal only if the selection term is zero."

**Common trap:** Do not infer harm just because participants do worse than nonparticipants. In the Maria/Khuzdar logic from lecture, the observed comparison can have the opposite sign from the causal effect if the treated group started from a worse counterfactual.

**Explain Like I'm 5:** Each person has two possible outcomes, but we only see one. Bias appears when we compare treated people to untreated people who were already different before treatment.

## 3. Random Assignment

**Core idea:** Random assignment is the cleanest way to solve selection because it makes treatment status independent of potential outcomes. Treated and control groups may not match perfectly in a finite sample, but in expectation they come from the same distribution. That is why a simple difference in means can identify a causal effect under randomization.

**How to recognize it on the exam:** Words like lottery, randomly assigned, experimental group, control group, balanced, or same population point here. The question may ask why randomization helps, what the difference in means estimates, or why baseline covariates should be balanced on average.

**Comparison being made:** Compare average outcomes for the assigned treatment group to average outcomes for the assigned control group. The comparison is credible because assignment was not chosen by the units and was not chosen based on their potential outcomes.

**Identifying assumption:** Treatment assignment `D_i` is independent of the pair of potential outcomes. In practice, also watch the distinction between assignment and actual take-up. If people assigned treatment do not all receive it, the assignment contrast is usually ITT rather than the effect of receiving treatment.

**Formula/notation:**

```text
D_i independent of (Y_i(1), Y_i(0)), with 0 < Pr(D_i = 1) < 1
E[Y_i(0) | D_i = 1] - E[Y_i(0) | D_i = 0] = 0
Under random assignment:
E[Y | D = 1] - E[Y | D = 0] = ATE
```

**Interpretation sentence:** "Because treatment was randomly assigned, the control group's average outcome estimates the treated group's missing untreated counterfactual in expectation."

**Common trap:** Do not require every baseline characteristic to be exactly equal after randomization. Random assignment balances in expectation; finite samples can still have chance imbalance.

**Explain Like I'm 5:** Random assignment is like shuffling before dealing cards. It does not make every hand identical, but it makes the groups fair enough that the average difference can be treated as the program's effect.

## 4. OLS and Regression Interpretation

**Core idea:** OLS chooses coefficients that minimize squared residuals. In a simple regression, the slope is the covariance between the regressor and outcome divided by the variance of the regressor. In multiple regression, each coefficient is a conditional association: the predicted change in the outcome for a one-unit increase in that regressor, holding the included right-hand-side variables fixed.

**How to recognize it on the exam:** Regression-output questions almost always want three things in order: identify the dependent variable, interpret the coefficient in units, and then say whether the coefficient has a causal interpretation. Look for language like "holding controls constant," "interpret beta," or "what does this coefficient mean?"

**Comparison being made:** OLS compares units with different values of `X_i`. Multiple regression narrows the comparison to units with the same included controls. That can approximate stratification, but only over variables actually in the model.

**Identifying assumption:** For a causal interpretation, the error term must be unrelated to the treatment or regressor after conditioning on included controls. In lecture notation, the key condition is mean independence of the error given the right-hand-side variables.

**Formula/notation:**

```text
Fitted value: Yhat_i = beta_hat_0 + beta_hat_1 X_i
Residual: uhat_i = Y_i - Yhat_i
Simple OLS slope: beta_hat_1 = Cov(X, Y) / Var(X)

Multiple regression:
Y_i = beta_0 + beta_1 D_i + beta_2 X_i + epsilon_i
Key causal condition: E(epsilon_i | D_i, X_i) = 0
```

**Visual aid:** The OLS diagram separates the fitted line from the residuals. The line summarizes the comparison; the causal interpretation still depends on the error term being unrelated to the regressor after controls.

[[VISUAL:ols]]

**Interpretation sentence:** "A one-unit increase in `D_i` is associated with `beta_1` more units of `Y_i`, holding the included controls fixed; this is causal only if no remaining omitted factor in the error is correlated with `D_i`."

**Common trap:** "Holding all else constant" means holding included variables constant, not literally all possible determinants of the outcome. A missing confounder can still bias the coefficient.

**Explain Like I'm 5:** OLS draws the best-fitting line through the data. The line is causal only when the leftover reasons people differ are not secretly tied to the variable you care about.

## 5. Dummy Variables, Interactions, and Demeaning

**Core idea:** Dummy variables turn categories into comparisons against a reference group. Interactions let a relationship differ across groups or across values of another variable. A dummy-by-dummy interaction is an extra joint effect beyond the two main effects. A continuous-by-dummy interaction changes the slope for one group. Demeaning moves the zero point of a continuous variable so the dummy main effect is evaluated at an average, meaningful baseline.

**How to recognize it on the exam:** Look for `factor(...)`, binary variables, group categories, terms with `*`, or questions asking for "the effect for this group." If a prompt asks about a subgroup, expect to add coefficients rather than point to a single row.

**Comparison being made:** The omitted category is the baseline. A dummy coefficient compares the named group to that baseline. An interaction coefficient compares whether the gap or slope for one group differs from the baseline group's gap or slope.

**Identifying assumption:** The same OLS exogeneity condition applies if the prompt asks for causality. The interaction changes what comparison is estimated; it does not solve selection or omitted variables by itself.

**Formula/notation:**

```text
Dummy interaction:
earnings_i = b0 + b1 female_i + b2 asian_i + b3(asian_i * female_i) + e_i

b1 = female gap among non-Asian workers
b2 = Asian male gap relative to non-Asian men
b3 = additional Asian-woman difference beyond b1 and b2

Demeaning:
IQ_tilde_i = IQ_i - mean(IQ)
Then b1 is the female gap at average IQ
```

**Interpretation sentence:** "For the interacted group, combine the relevant main effect and interaction term; the interaction alone is only the extra difference relative to the reference group."

**Common trap:** Do not interpret the interaction coefficient as the full group effect. Do not interpret a main effect without checking both the reference category and the zero point of the interacted continuous variable.

**Explain Like I'm 5:** Dummies tell you which group is being compared to the baseline. Interactions tell you whether that comparison changes for a particular group or at a particular value.

## 6. Selection on Observables, Conditional Independence Assumption (CIA), and Common Support

**Core idea:** When there is no random assignment, regression can be used as a structured comparison among units with the same observed covariates. The Conditional Independence Assumption (CIA) says that after conditioning on observed `X_i`, treatment is as good as randomly assigned. Common support says those within-`X_i` comparisons actually exist: for relevant covariate values, there are both treated and untreated units.

**How to recognize it on the exam:** Use this section for observational studies with controls, matching-style logic, or prompts that say "compare people with the same background characteristics." The private-university example is the lecture anchor: compare students with similar application sets or ability proxies who chose different college types.

**Comparison being made:** Treated and control units are compared within covariate cells or after regression adjustment for covariates. The comparison tries to replace a broad treated-control gap with like-versus-like comparisons.

**Identifying assumption:** All confounding must be captured by the observed controls. If unobserved motivation, ability, family background, networks, neighborhood conditions, or expectations still affect both treatment and outcomes, CIA fails. Common support additionally requires overlap so the method is not extrapolating beyond comparable data.

**Formula/notation:**

```text
CIA:
(Y_i(1), Y_i(0)) independent of D_i conditional on X_i

Common support:
0 < Pr(D_i = 1 | X_i) < 1
```

**Interpretation sentence:** "Conditional on the observed covariates, the untreated comparison units are being used as the treated units' missing counterfactual."

**Common trap:** Adding many controls is not the same as satisfying CIA. Controls only solve selection on observed variables, and lack of overlap means the regression is leaning on model extrapolation rather than real comparisons.

**Explain Like I'm 5:** Controls help only if they make treated and untreated people truly comparable. If the important difference is hidden or there is no similar untreated person, the comparison is still shaky.

## 7. OVB

**Core idea:** OVB happens when a left-out variable both affects the outcome and is correlated with the included regressor. The short regression then gives the included regressor credit or blame for variation that belongs to the omitted variable. The lecture's private-university example uses applicant-group quality or ability as the confounder: if higher-earning applicant groups are also more likely to attend private schools, the raw private-school coefficient is upward biased.

**How to recognize it on the exam:** Look for short-versus-long regressions, "direction of bias," "what happens when we omit ability/family background/location," or a prompt that gives an omitted variable's relationship with both treatment and outcome. The exam move is to sign the two links separately.

**Comparison being made:** The short regression compares treated and untreated units without holding the omitted variable fixed. The long regression adds the omitted variable and compares units with the same value of that omitted factor. The difference between those two coefficients is the bias.

**Identifying assumption:** The omitted variable must either be unrelated to the treatment/regressor or have no effect on the outcome. If both links are nonzero, the short regression is biased.

**Formula/notation:**

```text
Long regression:  Y_i = alpha_l + beta_l P_i + gamma A_i + epsilon_li
Short regression: Y_i = alpha_s + beta_s P_i + epsilon_si
Auxiliary regression: A_i = pi_0 + pi_1 P_i + u_i

OVB = beta_s - beta_l = pi_1 * gamma

Cov/Var version used in exercises:
c1 = Cov(Y, W) / Var(W)
c2 = Cov(W, X) / Var(X)
Bias = c1 * c2
```

**Visual aid:** The OVB diagram makes the sign logic mechanical. Bias requires one path from the omitted variable to the treatment/regressor and another path from the omitted variable to the outcome.

[[VISUAL:ovb]]

**Interpretation sentence:** "The short coefficient equals the controlled coefficient plus the part of the omitted variable's outcome effect that is mechanically loaded onto the included regressor."

**Common trap:** Do not memorize only "positive omitted variable means upward bias." The sign depends on the product of two relationships: omitted variable with treatment, and omitted variable with outcome.

**Explain Like I'm 5:** OVB is blame getting assigned to the wrong variable. If a missing factor is tied to both the treatment and the outcome, the coefficient mixes the treatment effect with that missing factor.

## 8. Simultaneity and Measurement Error

**Core idea:** Simultaneity is a feedback problem: the regressor affects the outcome, but the outcome also affects the regressor. The police/crime example is the lecture anchor because police may reduce crime, while high crime also causes more police deployment. Measurement error is a data-quality problem: the true regressor is observed with noise. Classical measurement error in the regressor pushes the coefficient toward zero.

**How to recognize it on the exam:** Use simultaneity when the causal arrow plausibly runs both ways. Use measurement error when a key variable is self-reported, misclassified, proxied, or counted with noise.

**Comparison being made:** In simultaneity, OLS compares units with different observed `X_i`, but part of that difference in `X_i` is itself a response to `Y_i` or the shocks inside the error term. In measurement error, OLS compares units using noisy measured values rather than the true values, so the signal is diluted.

**Identifying assumption:** For simultaneity, exogeneity fails because the regressor is correlated with the error. For classical measurement error, the observed regressor equals true signal plus noise, and that noise weakens the relationship between observed `X_i` and `Y_i`.

**Formula/notation:**

```text
Endogeneity:
E(epsilon_i | X_i) != 0

Simultaneity example:
Y_1 = alpha_1 Y_2 + beta_1 Z_1 + mu_1
Y_2 = alpha_2 Y_1 + beta_2 Z_2 + mu_2

Classical measurement error:
S_i = S_i* + m_i
beta_hat_bad = r * beta
r = Var(S_i*) / [Var(S_i*) + Var(m_i)], where 0 < r < 1
```

**Interpretation sentence:** "The coefficient is not isolating the effect of `X_i` on `Y_i` because either `Y_i` also helps determine `X_i`, or the measured `X_i` is a noisy stand-in for the true regressor."

**Common trap:** Adding ordinary controls does not automatically fix simultaneity. The issue is reciprocal causation, not just a missing background variable. For measurement error, remember attenuation: the estimate is biased toward zero, not necessarily toward a negative number.

**Explain Like I'm 5:** Simultaneity is a two-way street, so OLS cannot tell which direction caused what. Measurement error is a blurry ruler, so the measured relationship usually looks weaker than the real one.

## 9. Bad Controls and Post-Treatment Bias

**Core idea:** More controls are not always better. A bad control is a variable that is itself affected by treatment, especially a mediator between treatment and outcome. Controlling for it blocks part of the causal pathway and changes the estimand. In the job-training example, later employment is not a clean pre-treatment control if training affects employment and employment affects earnings.

**How to recognize it on the exam:** Watch for proposed controls measured after treatment or variables that treatment plausibly causes: employment after training, income after schooling, health status after insurance, or any "intermediate outcome." The exam may ask whether to control for the variable or why adding it changes the coefficient.

**Comparison being made:** With the bad control included, the regression compares treated and untreated units with the same value of a post-treatment variable. That is no longer the total effect comparison; it holds fixed part of what treatment may have changed.

**Identifying assumption:** A valid control should be predetermined relative to treatment and should help block confounding paths. A post-treatment control violates that logic because it lies downstream of treatment.

**Formula/notation:**

```text
Treatment: Z
Mediator/post-treatment variable: S = Z + error_S
Outcome: Y = Z + S + error_Y

Total effect of Z on Y = direct path from Z to Y + indirect path through S
Controlling for S blocks the indirect path
```

**Visual aid:** The bad-control diagram marks the danger: if treatment causes the control, holding it fixed changes the question from total effect to a direct-effect comparison.

[[VISUAL:bad_controls]]

**Interpretation sentence:** "After controlling for the mediator, the coefficient is closer to a direct-effect comparison among units with the same post-treatment value, not the total policy effect."

**Common trap:** A variable can be predictive and still be a bad control. The question is not whether it predicts the outcome; the question is whether treatment caused it.

**Explain Like I'm 5:** Do not control for something that happens after the treatment if the treatment may have caused it. That is like judging a path while blocking part of the path you wanted to measure.

## 10. IV and 2SLS

**Core idea:** IV is used when the treatment or regressor is endogenous because of OVB, simultaneity, or measurement error. The instrument `Z_i` supplies external variation in the endogenous variable `X_i`. The first stage asks whether `Z_i` moves `X_i`. The reduced form asks whether `Z_i` moves `Y_i`. The exclusion restriction says the only reason `Z_i` moves `Y_i` is that it moves `X_i`.

**How to recognize it on the exam:** Prompts about rainfall, lotteries, draft numbers, vouchers, weak instruments, or "instrument validity" point here. If the question asks whether an instrument is valid, state first stage and exclusion in words tied to the case before writing formulas.

**Comparison being made:** IV compares outcome differences generated by instrument-induced changes in the endogenous regressor. 2SLS implements the same logic by first predicting `X_i` using the instrument and then using that predicted component in the outcome equation.

**Identifying assumption:** The instrument must be relevant, meaning it has a nonzero first stage, and excludable, meaning it affects the outcome only through the endogenous regressor. In L5, first-stage strength can be checked in the data; exclusion is a design claim defended with domain knowledge.

**Formula/notation:**

```text
Structural equation:
Y_i = alpha + rho X_i + eta_i

First stage:
X_i = pi_0 + pi_1 Z_i + u_i

IV/Wald estimand:
rho = Cov(Y_i, Z_i) / Cov(X_i, Z_i)
Equivalent binary form: Reduced Form / First Stage

2SLS:
1st stage: X_i = pi_0 + pi_1 Z_i + u_i, get Xhat_i
2nd stage: Y_i = alpha + rho Xhat_i + v_i

R pattern:
ivreg(Y ~ X1 + X2 | Z + X2, data = dat)
```

**Visual aid:** The IV pipeline shows the exam sequence: prove the instrument moves treatment, show assignment moves the outcome, then divide reduced form by first stage.

[[VISUAL:iv_pipeline]]

**Interpretation sentence:** "The IV estimate is the effect of `X_i` on `Y_i` for the variation in `X_i` that is induced by the instrument, assuming the instrument has no direct path to the outcome."

**Common trap:** A strong first stage does not prove exclusion. A weak first stage makes the denominator small, so estimates become volatile and any exclusion violation can be amplified. L5 notes the old `F > 10` rule of thumb and newer stricter weak-instrument concerns.

**Explain Like I'm 5:** An instrument is useful when it nudges treatment for reasons unrelated to the outcome except through treatment. First stage asks whether the nudge works; exclusion asks whether the nudge has only that one path.

## 11. ITT, TOT, Compliance Types, and LATE

**Core idea:** L6 separates assignment from take-up. A lottery or offer may change the probability of treatment without perfectly determining treatment. ITT is the effect of assignment or offer. TOT is the effect of actually receiving treatment among takers in one-sided compliance settings. LATE is the effect for compliers, the people whose treatment status changes because of the assignment or instrument.

**How to recognize it on the exam:** Use this section for lotteries, scholarships, vouchers, offers, eligibility rules, or any program where some assigned units do not take treatment and some nonassigned units may still get treatment. The PACES voucher example is the lecture anchor.

**Comparison being made:** ITT compares outcomes by assignment `Z_i`, regardless of actual take-up `D_i`. The first stage compares take-up by assignment. The Wald ratio divides the outcome effect of assignment by the take-up effect of assignment, rescaling the assignment contrast into a complier treatment-effect estimate.

**Identifying assumption:** For LATE, assignment must be as good as random, the first stage must be nonzero, the exclusion restriction must hold, and monotonicity must rule out defiers. Under one-sided compliance, a simple TOT scaling is available because no one in the control group receives treatment.

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
LATE = [E(Y | Z = 1) - E(Y | Z = 0)] /
       [E(D | Z = 1) - E(D | Z = 0)]
     = Reduced Form / First Stage

With monotonicity:
p_A = Pr(D = 1 | Z = 0)
p_N = Pr(D = 0 | Z = 1)
p_C = Pr(D = 1 | Z = 1) - Pr(D = 1 | Z = 0)
```

**Visual aid:** The compliance table keeps the four principal strata separate. The LATE interpretation belongs to compliers, because they are the group whose treatment status changes when assignment changes.

[[VISUAL:compliance]]

**Interpretation sentence:** "The Wald ratio estimates the treatment effect for compliers: the units whose treatment status is moved by the assignment."

**Common trap:** Do not call LATE the ATE. Always-takers and never-takers help determine take-up shares, but they do not identify the treatment effect because assignment does not change their treatment status.

**Explain Like I'm 5:** With noncompliance, the lottery only changes treatment for some people. LATE is the effect for those people, the compliers, not for everyone in the study.

## 12. IV Identification Assumptions Under Potential Outcomes

**Core idea:** L6 rewrites IV in potential-outcomes terms. The AIR framework says the instrument identifies a complier average causal effect when four conditions hold: random assignment of the instrument, a nonzero first stage, exclusion, and monotonicity. This is the formal bridge between the intuitive Wald ratio and the LATE interpretation.

**How to recognize it on the exam:** Use this when a prompt asks for IV assumptions, what IV identifies, or what the exclusion restriction means. The best answer gives the formal assumption and then translates it into the case.

**Comparison being made:** The instrument splits units into `Z_i = 1` and `Z_i = 0` groups. The reduced form compares their outcomes. The first stage compares their treatment rates. The LATE theorem says the ratio of those two assignment-induced differences isolates compliers under the AIR assumptions.

**Identifying assumption:** The instrument must be randomly assigned relative to all relevant potential outcomes and compliance types; it must move treatment for some units; it must affect the outcome only through treatment; and it must not make anyone move opposite the instrument.

**Formula/notation:**

```text
Random assignment:
({Y_i(d,z) for all d,z}, D_1i, D_0i) independent of Z_i

First stage:
E[D_i | Z_i = 1] - E[D_i | Z_i = 0] != 0

Exclusion:
Y_i(d,0) = Y_i(d,1) = Y_di for d = 0,1

Monotonicity:
D_1i - D_0i >= 0 for all i

LATE theorem:
rho_C = [E(Y | Z = 1) - E(Y | Z = 0)] /
        [E(D | Z = 1) - E(D | Z = 0)]
```

**Visual aid:** The assumption checklist pairs each major method with its causal assumption and the most common failure cue.

[[VISUAL:assumptions]]

**Interpretation sentence:** "If assignment is random, moves treatment, affects outcomes only through treatment, and has no defiers, the Wald ratio is the causal effect for compliers."

**Common trap:** Random assignment of the instrument is not random assignment of treatment. Exclusion is usually the fragile assumption. Placebo tests and covariate balance checks can support the story, but they do not mechanically prove exclusion.

**Explain Like I'm 5:** IV works only if the instrument is fair, actually moves treatment, has no side door to the outcome, and never pushes anyone the opposite way. If those hold, the Wald ratio tells you the complier effect.

## Final One-Page Memory Check

- **Potential outcomes:** Ask which counterfactual is missing before interpreting a group difference.
- **Random assignment:** Difference in means is causal because selection bias is zero in expectation.
- **OLS:** Interpret in outcome units, then ask whether the error is unrelated to the regressor after controls.
- **Dummy variables and interactions:** Main effects depend on the reference group and zero point; subgroup effects often require adding coefficients.
- **CIA/common support:** Regression adjustment works only if treated and control units are comparable on observed covariates and overlap exists.
- **OVB:** Bias equals the omitted-treatment relationship times the omitted-outcome relationship.
- **Simultaneity:** Feedback between `X_i` and `Y_i` makes the regressor endogenous.
- **Measurement error:** Classical noise in the regressor attenuates the coefficient toward zero.
- **Bad controls:** Do not control for variables caused by treatment unless you intentionally want a direct-effect or mediated-effect estimand.
- **IV:** First stage makes the instrument relevant; exclusion makes it valid; weak first stage makes estimates unstable.
- **LATE:** With noncompliance, IV estimates the effect for compliers, not everyone.

---
Generated for: Edgar Agunias
Date: 2026-04-30
Model: GPT-5 (Codex, reasoning effort not exposed)
Sources: QM3 lecture slides L1-L6 (`QM3_L1_Intro.pdf`, `QM3_L2_CaInf.pdf`, `QM3_L3_Reg.pdf`, `QM3_L4_Reg2.pdf`, `QM3_L5_IV.pdf`, `QM3_L6_IV2.pdf`); `QM3_Midterm_Lecture_Reference_v1.2.0_notes.md`; original code-generated visual aids; Tyche memory files
Agent: Tyche
---
