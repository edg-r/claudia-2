# ======================================================================
#  GPEC 446 — Lab 7: Evaluating a Randomised Controlled Trial
#  Application: Mexico's Progresa Programme and Electoral Outcomes
#  Reference: de la O (2013), AJPS
# ======================================================================

library(tidyverse)
library(estimatr)
library(modelsummary)
library(rdrobust)


# ======================================================================
# 1. DATA
# ======================================================================

# Progresa (now Oportunidades/Prospera) was a conditional cash transfer
# programme targeting poor rural households in Mexico. The government
# randomised at the LOCALITY level: 314 localities received the programme
# immediately, 186 were assigned to delayed entry.
#
# This dataset aggregates to the precinct level (417 precincts) and asks
# whether Progresa affected electoral behaviour — specifically, whether
# communities that received transfers voted more for the ruling PRI.

progresa <- read.csv(
  "https://raw.githubusercontent.com/kosukeimai/qss/master/PREDICTION/progresa.csv"
)

dim(progresa)      # 417 precincts, 20 variables
table(progresa$treatment)

# Key variables:
#   treatment   = 1 if precinct contains a village with early Progresa
#   pri2000s    = PRI vote share (2000), as share of pop 18+
#   pri2000v    = official PRI vote share (2000)
#   t2000/t2000r = turnout (2000), two measures
#   pri1994v    = PRI vote share (1994) — BASELINE
#   pan1994v    = PAN vote share (1994) — BASELINE
#   prd1994v    = PRD vote share (1994) — BASELINE
#   t1994r      = turnout (1994) — BASELINE
#   avgpoverty  = precinct average poverty index
#   pobtot1994  = total population (1994)
#   villages    = number of villages in precinct


# ======================================================================
# 2. BALANCE TESTING
# ======================================================================

# Randomisation ensures balance IN EXPECTATION, but any single draw can
# produce accidental imbalance. We check by comparing pre-treatment
# (1994) characteristics across groups.

# Simple comparison of means
progresa %>%
  group_by(treatment) %>%
  summarise(
    n         = n(),
    pri1994   = mean(pri1994v, na.rm = TRUE),
    pan1994   = mean(pan1994v, na.rm = TRUE),
    prd1994   = mean(prd1994v, na.rm = TRUE),
    turnout94 = mean(t1994r,   na.rm = TRUE),
    poverty   = mean(avgpoverty, na.rm = TRUE),
    pop       = mean(pobtot1994, na.rm = TRUE),
    villages  = mean(villages, na.rm = TRUE)
  )

# Formal balance test: regress each baseline variable on treatment.
# A significant coefficient signals imbalance.
baseline_vars <- c("pri1994v", "pan1994v", "prd1994v",
                    "t1994r", "avgpoverty", "pobtot1994", "villages")

balance_models <- map(baseline_vars, ~ lm(
  as.formula(paste(.x, "~ treatment")), data = progresa
))
names(balance_models) <- baseline_vars

modelsummary(
  balance_models,
  stars = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  coef_map = c("treatment" = "Treatment"),
  gof_map = c("nobs", "r.squared"),
  title = "Balance Test: Baseline Covariates on Treatment Assignment"
)


# ======================================================================
# 3. ESTIMATING THE ATE
# ======================================================================

# Under random assignment, the difference in sample means is an unbiased
# estimator of the ATE: tau_hat = Y_bar(1) - Y_bar(0).
# OLS on Y ~ D recovers the same number.

# --- 3a. Difference in means -----------------------------------------
t.test(pri2000s ~ treatment, data = progresa)

# --- 3b. OLS (equivalent) --------------------------------------------
mod_simple <- lm(pri2000s ~ treatment, data = progresa)

# --- 3c. Adding baseline controls ------------------------------------
# Controls are NOT needed for unbiasedness (randomisation already ensures
# that), but they absorb residual variance and tighten standard errors.
# The point estimate should barely change if randomisation worked.

mod_controls <- lm(
  pri2000s ~ treatment + pri1994v + pan1994v + prd1994v +
    t1994r + avgpoverty + pobtot1994 + villages,
  data = progresa
)

modelsummary(
  list("No Controls" = mod_simple, "With Controls" = mod_controls),
  stars = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  coef_map = c(
    "treatment"  = "Treatment",
    "pri1994v"   = "PRI Vote 1994",
    "pan1994v"   = "PAN Vote 1994",
    "prd1994v"   = "PRD Vote 1994",
    "t1994r"     = "Turnout 1994",
    "avgpoverty" = "Avg Poverty",
    "pobtot1994" = "Population 1994",
    "villages"   = "No. Villages"
  ),
  gof_map = c("nobs", "r.squared", "adj.r.squared"),
  title = "Effect of Progresa on PRI Vote Share (2000)"
)


# ======================================================================
# 4. ROBUST STANDARD ERRORS
# ======================================================================

# Classical OLS SEs assume homoskedasticity. HC2 robust SEs relax this.
# In general, cluster SEs at the level of randomisation (here, locality).

mod_robust <- lm_robust(
  pri2000s ~ treatment + pri1994v + pan1994v + prd1994v +
    t1994r + avgpoverty + pobtot1994 + villages,
  data = progresa, se_type = "HC2"
)

modelsummary(
  list("Classical SEs" = mod_controls, "Robust (HC2)" = mod_robust),
  stars = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  coef_map = c("treatment" = "Treatment"),
  gof_map = c("nobs", "r.squared"),
  title = "Classical vs Robust Standard Errors"
)


# ======================================================================
# 5. MULTIPLE OUTCOMES
# ======================================================================

# RCTs often examine several outcomes. Here we check whether Progresa
# affected PRI vote share, turnout, or both.

mod_pri     <- lm_robust(pri2000s ~ treatment, data = progresa, se_type = "HC2")
mod_turnout <- lm_robust(t2000    ~ treatment, data = progresa, se_type = "HC2")
mod_pri_v   <- lm_robust(pri2000v ~ treatment, data = progresa, se_type = "HC2")
mod_turn_v  <- lm_robust(t2000r   ~ treatment, data = progresa, se_type = "HC2")

modelsummary(
  list("PRI (pop)" = mod_pri,   "Turnout (pop)" = mod_turnout,
       "PRI (off)" = mod_pri_v, "Turnout (off)"  = mod_turn_v),
  stars = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  coef_map = c("treatment" = "Treatment"),
  gof_map = c("nobs", "r.squared"),
  title = "Treatment Effects Across Electoral Outcomes"
)


# ======================================================================
# 6. HETEROGENEOUS EFFECTS
# ======================================================================

# Does the treatment effect differ by poverty level? We interact
# treatment with a median split on the poverty index.

progresa <- progresa %>%
  mutate(high_poverty = as.integer(
    avgpoverty >= median(avgpoverty, na.rm = TRUE)))

mod_base   <- lm_robust(pri2000s ~ treatment,
                         data = progresa, se_type = "HC2")
mod_hetero <- lm_robust(pri2000s ~ treatment * high_poverty,
                         data = progresa, se_type = "HC2")

modelsummary(
  list("Pooled" = mod_base, "By Poverty" = mod_hetero),
  stars = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  coef_map = c(
    "treatment"                = "Treatment",
    "high_poverty"             = "High Poverty",
    "treatment:high_poverty"   = "Treatment x High Poverty"
  ),
  gof_map = c("nobs", "r.squared"),
  title = "Heterogeneous Effects by Poverty Level"
)


# ======================================================================
# 7. NON-COMPLIANCE: ITT vs LATE
# ======================================================================

# In a perfect experiment, assignment = receipt. In practice, some units
# assigned to treatment don't take it up ("never-takers"), and some
# controls access similar programmes ("always-takers").
#
# This creates two estimands:
#   ITT  = effect of ASSIGNMENT  (diluted by non-compliance)
#   LATE = effect of RECEIPT for compliers
#
# LATE is recovered by using assignment (Z) as an instrument for actual
# take-up (D). This is the Wald estimator: LATE = ITT / First Stage.

# Simulate imperfect compliance (the dataset only records assignment)
set.seed(446)

progresa_nc <- progresa %>%
  mutate(
    assigned = treatment,
    # 80% of treated comply; 5% of controls access similar programmes
    takeup = case_when(
      assigned == 1 ~ rbinom(n(), 1, prob = 0.80),
      assigned == 0 ~ rbinom(n(), 1, prob = 0.05)
    ),
    # Simulated outcome: true effect of take-up = 0.03
    y_sim = 0.30 + 0.03 * takeup + 0.5 * avgpoverty +
      rnorm(n(), 0, 0.05)
  )

# Compliance rates
progresa_nc %>%
  group_by(assigned) %>%
  summarise(n = n(), pct_takeup = mean(takeup))

# Three estimators:
#   ITT   — regress outcome on assignment (unbiased for ITT, not for ATE)
#   Naive — regress outcome on take-up (biased: selection into take-up)
#   LATE  — IV: instrument take-up with assignment (unbiased for LATE)
mod_itt   <- lm_robust(y_sim ~ assigned, data = progresa_nc, se_type = "HC2")
mod_naive <- lm_robust(y_sim ~ takeup,   data = progresa_nc, se_type = "HC2")
mod_iv    <- iv_robust(y_sim ~ takeup | assigned,
                       data = progresa_nc, se_type = "HC2")

modelsummary(
  list("ITT" = mod_itt, "Naive" = mod_naive, "LATE (IV)" = mod_iv),
  stars = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  coef_map = c("assigned" = "Assigned", "takeup" = "Take-up"),
  gof_map = c("nobs"),
  title = "ITT vs Naive vs LATE"
)

# Manual Wald estimator: LATE = ITT / First Stage
itt_hat  <- mean(progresa_nc$y_sim[progresa_nc$assigned == 1]) -
            mean(progresa_nc$y_sim[progresa_nc$assigned == 0])
fs_hat   <- mean(progresa_nc$takeup[progresa_nc$assigned == 1]) -
            mean(progresa_nc$takeup[progresa_nc$assigned == 0])

cat("ITT:         ", round(itt_hat, 4), "\n")
cat("First stage: ", round(fs_hat, 4), "\n")
cat("LATE = ITT/FS:", round(itt_hat / fs_hat, 4), "\n")
cat("True effect:  0.03\n")


# ======================================================================
# 8. FUZZY RDD: MAIMONIDES' RULE (Angrist & Lavy, 1999)
# ======================================================================

# Non-compliance in an RCT is solved by instrumenting take-up with
# assignment. Fuzzy RDD is the same idea in a discontinuity setting:
# crossing the cutoff changes the PROBABILITY of treatment (first
# stage < 1), so we scale the reduced form by the first stage.
#
# Sharp RDD:  D_i = 1(X_i >= x_0)        => first stage = 1
# Fuzzy RDD:  P(D_i=1) jumps at x_0      => first stage < 1
# Estimator:  alpha_frdd = reduced form / first stage  (= Wald / IV)
#
# Application: Maimonides' Rule in Israeli schools.
# The rule caps class size at 40. A 5th grade with 41 students must
# split into two classes of ~20. But compliance is imperfect: some
# schools above 40 don't split, and some below 40 split early.
# So crossing 40 changes the PROBABILITY of a small class — fuzzy RDD.

# install.packages("DOS")
library(DOS)
data(angristlavy)

# cohsize  = 5th-grade enrolment (running variable)
# numclass = number of classes (1 or 2)
# clasz    = actual average class size
# avgmath  = average math score (outcome)
# avgverb  = average verbal score (outcome)
# tipuach  = percent disadvantaged students

# Treatment: school split into 2+ classes (→ smaller class size)
angristlavy <- angristlavy %>%
  mutate(
    split   = as.integer(numclass >= 2),
    above40 = as.integer(cohsize > 40),
    cohsize_c = cohsize - 40            # centre the running variable
  )

# --- 8a. First stage: does crossing 40 cause splitting? ---------------

# Compliance is imperfect — this is what makes it fuzzy
angristlavy %>%
  group_by(above40) %>%
  summarise(
    n = n(),
    pct_split     = mean(split),
    avg_classsize = mean(clasz)
  )

# First-stage plot: P(split) against enrolment
ggplot(angristlavy, aes(x = cohsize, y = split)) +
  geom_point(alpha = 0.4) +
  geom_vline(xintercept = 40, linetype = "dashed", colour = "red") +
  geom_smooth(data = filter(angristlavy, cohsize <= 40),
              method = "lm", se = FALSE, colour = "steelblue") +
  geom_smooth(data = filter(angristlavy, cohsize > 40),
              method = "lm", se = FALSE, colour = "steelblue") +
  labs(x = "5th-Grade Enrolment", y = "P(Class Split)",
       title = "First Stage: Maimonides' Rule") +
  theme_minimal()

# --- 8b. Reduced form: does crossing 40 affect test scores? -----------

ggplot(angristlavy, aes(x = cohsize, y = avgmath)) +
  geom_point(alpha = 0.4) +
  geom_vline(xintercept = 40, linetype = "dashed", colour = "red") +
  geom_smooth(data = filter(angristlavy, cohsize <= 40),
              method = "lm", se = TRUE, colour = "steelblue") +
  geom_smooth(data = filter(angristlavy, cohsize > 40),
              method = "lm", se = TRUE, colour = "steelblue") +
  labs(x = "5th-Grade Enrolment", y = "Average Math Score",
       title = "Reduced Form: Math Scores at the Cutoff") +
  theme_minimal()

# --- 8c. Parametric fuzzy RDD (IV approach) --------------------------

# With a modest sample (172 matched schools), we use a parametric
# local-linear specification rather than nonparametric rdrobust.
# The instrument is above40 = 1(cohsize > 40).
# We control for the running variable (centred at 40) with separate
# slopes on each side.

# First stage: does above40 predict split?
fs <- lm_robust(
  split ~ above40 * cohsize_c,
  data = angristlavy, se_type = "HC2"
)

# Reduced form: does above40 predict math scores?
rf <- lm_robust(
  avgmath ~ above40 * cohsize_c,
  data = angristlavy, se_type = "HC2"
)

# Fuzzy RDD via IV: instrument split with above40
# This is exactly 2SLS, the same logic as Section 7
mod_fuzzy <- iv_robust(
  avgmath ~ split * cohsize_c | above40 * cohsize_c,
  data = angristlavy, se_type = "HC2"
)

modelsummary(
  list("First Stage" = fs, "Reduced Form" = rf, "Fuzzy RDD (IV)" = mod_fuzzy),
  stars = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  coef_map = c(
    "above40"          = "Above 40",
    "split"            = "Class Split (instrumented)",
    "cohsize_c"        = "Enrolment (centred)",
    "above40:cohsize_c" = "Above 40 x Enrolment",
    "split:cohsize_c"  = "Split x Enrolment"
  ),
  gof_map = c("nobs", "r.squared"),
  title = "Fuzzy RDD: Maimonides' Rule — First Stage, Reduced Form, and IV"
)

# --- 8d. Nonparametric fuzzy RDD with rdrobust -------------------------

# rdrobust uses local-polynomial regression with a data-driven bandwidth.
# It does NOT assume a global linear relationship — it fits polynomials
# in a narrow window around the cutoff selected by MSE-optimal criteria.
#
# With only 172 observations (and the DOS data already restricted to
# matched pairs near the cutoff), rdrobust selects very narrow bandwidths
# that leave few effective observations on each side. The result: large
# standard errors and no significance — even if the parametric IV above
# finds a significant effect.
#
# This is NOT a contradiction. The parametric model borrows strength from
# the full sample by assuming linearity in the running variable. rdrobust
# makes weaker assumptions (local smoothness only) and pays for that
# flexibility with wider confidence intervals when data is sparse near
# the cutoff. In large samples (thousands of observations), the two
# approaches converge. In small samples, the parametric model is more
# powerful but more assumption-dependent.

library(rdrobust)

# Sharp RDD (ignores imperfect compliance)
rd_sharp <- rdrobust(angristlavy$avgmath, angristlavy$cohsize, c = 40)
summary(rd_sharp)

# Fuzzy RDD: instrument split with 1(cohsize > 40) internally
rd_fuzzy <- rdrobust(
  y = angristlavy$avgmath,
  x = angristlavy$cohsize,
  c = 40,
  fuzzy = angristlavy$split
)
summary(rd_fuzzy)

# Note: effective N is very small (~20 per side) → wide CIs.
# The point estimate should be roughly consistent with the parametric
# IV above, but the standard errors will be much larger.
# Lesson: nonparametric methods are honest about uncertainty when
# data is scarce, but require large samples to be informative.
