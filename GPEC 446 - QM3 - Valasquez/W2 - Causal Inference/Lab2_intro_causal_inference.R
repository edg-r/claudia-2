# =============================================================================
#  GPEC 446 — Lab 2: Regression for Causal Inference
#  Stratification, Omitted Variable Bias, and Simultaneity
#  David L. Vargas
#  Last modified: 04.09.2026
# =============================================================================
#
#  Last week we saw that a randomised experiment makes causal estimation
#  straightforward: just compare group means.  But most policy questions
#  cannot be answered with an experiment.  When treatment is NOT randomly
#  assigned, we need regression — and we need to think carefully about
#  what it can and cannot do.
#
#  This lab covers three ideas:
#
#    1. Regression as stratification — how controlling for covariates
#       makes within-group comparisons automatically
#    2. Omitted variable bias — what goes wrong when we leave out a
#       confounder, and how to quantify it
#    3. Simultaneity — what happens when causation runs both ways
#
#
#  Data:
#    - UC Berkeley admissions (1973) for Section 1
#    - California school districts (CASchools, AER package) for Section 2
#    - Simulated police/crime data for Section 3
#
# =============================================================================


# -----------------------------------------------------------------------------
# Recap from Lab 1
# -----------------------------------------------------------------------------
#
#  In Lab 1, we used the Tennessee STAR experiment to estimate the causal
#  effect of small classes on test scores.  A key finding: adding controls
#  (free lunch, ethnicity, gender) barely changed the treatment coefficient.
#
#  Why?  Because RANDOMISATION already made the groups comparable.
#  Controls improved precision (smaller standard errors) but did not
#  shift the point estimate — there was no bias to remove.
#
#  This will NOT be true in observational settings.  When treatment is
#  not randomly assigned, the controls we include (or omit) can change
#  the estimate dramatically — and can even flip the sign.
# -----------------------------------------------------------------------------

library(AER)
library(tidyverse)
library(stargazer)


# =============================================================================
# SECTION 1 — Regression as Stratification
# =============================================================================
#
#  In 1973, the University of California, Berkeley was sued for gender
#  discrimination in graduate admissions.  The overall numbers looked
#  damning: 44% of male applicants were admitted, but only 30% of
#  female applicants.  A gap of 14 percentage points.
#
#  But was this really discrimination?  Or could the gap be explained
#  by something else?
#
# --- 1a. Load and explore the data ---
#
#  UCBAdmissions
#  It contains admission decisions for 4,526 applicants across
#  6 departments (A through F), by gender.

data("UCBAdmissions")

# Convert the table to a data frame for easier manipulation
ucb <- as.data.frame(UCBAdmissions)

# What does the data look like?
print(ucb)

#  Each row is a combination of Admit (Admitted/Rejected),
#  Gender (Male/Female), and Dept (A–F), with Freq = count.


# --- 1b. The overall admission rates ---
#
#  First, let's compute the NAIVE comparison: overall admission
#  rates by gender, ignoring department.

overall <- ucb %>%
  group_by(Gender) %>%
  summarise(
    applied  = sum(Freq),
    admitted = sum(Freq[Admit == "Admitted"]),
    rate     = admitted / applied,
    .groups  = "drop"
  )

print(overall)
cat("\nOverall admission rate (Male):  ",
    round(overall$rate[overall$Gender == "Male"] * 100, 1), "%\n")
cat("Overall admission rate (Female):",
    round(overall$rate[overall$Gender == "Female"] * 100, 1), "%\n")
cat("Gap:", round((overall$rate[overall$Gender == "Male"] -
                    overall$rate[overall$Gender == "Female"]) * 100, 1),
    "percentage points\n")

#  This looks like strong evidence of discrimination against women.
#  But let's dig deeper.


# --- 1c. Stratification by hand: within-department comparisons ---
#
#  Now let's compute admission rates WITHIN each department.  If the
#  overall gap is driven by discrimination, we should see it in every
#  department.  If it is driven by where men and women apply, the
#  within-department gaps should be much smaller — or even reversed.

by_dept <- ucb %>%
  group_by(Dept, Gender) %>%
  summarise(
    applied  = sum(Freq),
    admitted = sum(Freq[Admit == "Admitted"]),
    rate     = admitted / applied,
    .groups  = "drop"
  )

# Reshape to make it easy to compare male vs. female side by side
dept_comparison <- by_dept %>%
  select(Dept, Gender, applied, rate) %>%
  pivot_wider(
    names_from  = Gender,
    values_from = c(applied, rate)
  ) %>%
  mutate(
    gap = rate_Male - rate_Female,
    pct_female = applied_Female / (applied_Male + applied_Female)
  )

print(dept_comparison)

cat("\nWithin-department gaps (Male rate - Female rate):\n")
for (i in 1:nrow(dept_comparison)) {
  d <- dept_comparison[i, ]
  direction <- ifelse(d$gap > 0, "favours men", "favours women")
  cat("  Dept", as.character(d$Dept), ":",
      sprintf("%+.1f pp", d$gap * 100), paste0("(", direction, ")"),
      "  — Female applicants:",
      round(d$pct_female * 100), "%\n")
}

#  QUESTION: In how many departments do women have a HIGHER admission
#  rate than men?  What does this tell you about the "discrimination"
#  claim?
#
#  QUESTION: Look at the "% Female applicants" column.  Which
#  departments do women disproportionately apply to?  Are those the
#  departments with high or low overall admission rates?


# --- 1d. Visualising Simpson's Paradox ---

# Compute overall department admission rates (for both genders combined)
dept_overall <- ucb %>%
  group_by(Dept) %>%
  summarise(
    total_applied  = sum(Freq),
    total_admitted = sum(Freq[Admit == "Admitted"]),
    overall_rate   = total_admitted / total_applied,
    .groups = "drop"
  )

by_dept <- by_dept %>%
  left_join(dept_overall %>% select(Dept, overall_rate), by = "Dept")

ggplot(by_dept, aes(x = Dept, y = rate, fill = Gender)) +
  geom_col(position = "dodge") +
  geom_text(aes(label = applied), position = position_dodge(width = 0.9),
            vjust = -0.3, size = 3) +
  labs(
    title    = "UC Berkeley Admissions by Department and Gender (1973)",
    subtitle = "Numbers above bars = total applicants. Women applied to harder departments.",
    x        = "Department",
    y        = "Admission Rate",
    fill     = NULL
  ) +
  scale_y_continuous(labels = scales::percent_format()) +
  theme_minimal() +
  theme(legend.position = "bottom")

#  Departments A and B have high admission rates — and are mostly
#  male applicants.  Departments E and F are very competitive — and
#  have a higher share of female applicants.  This COMPOSITION EFFECT
#  is what drives the overall gap.


# --- 1e. Regression does the same thing automatically ---
#
#  To run a regression, we need individual-level data (one row per
#  applicant, not one row per group).  Let's expand the data.

ucb_individual <- ucb %>%
  uncount(Freq) %>%
  mutate(
    admitted = as.numeric(Admit == "Admitted"),
    female   = as.numeric(Gender == "Female")
  )

cat("\nTotal applicants:", nrow(ucb_individual), "\n")

# Naive regression: admitted ~ female (no department controls)
reg_naive <- lm(admitted ~ female, data = ucb_individual)

# Controlled regression: admitted ~ female + department dummies
reg_dept  <- lm(admitted ~ female + Dept, data = ucb_individual)

stargazer(reg_naive, reg_dept,
          type = "text",
          title = "UC Berkeley Admissions: Naive vs. Stratified",
          column.labels = c("No Controls", "Controlling for Dept"),
          dep.var.labels = "Admitted (0/1)",
          covariate.labels = c("Female", "Dept B", "Dept C",
                               "Dept D", "Dept E", "Dept F"),
          omit.stat = c("f", "ser", "adj.rsq"),
          notes = c("Dept A is the reference category.",
                    "Naive regression suggests bias against women.",
                    "Adding department controls reverses the sign."))

#  Look at the coefficient on "Female":
#    - Column 1 (naive): negative and significant — women are less
#      likely to be admitted.
#    - Column 2 (with dept controls): the coefficient flips sign or
#      shrinks dramatically.
#
#  The sign REVERSAL is Simpson's Paradox.  The "bias" was not in
#  how departments treated women — it was in WHERE women applied.
#
#  KEY INSIGHT: regression as stratification means regression compares
#  treated and control units with the SAME observed characteristics.
#  Here, it compares men and women who applied to the SAME department.
#
#  But — and this is crucial — it only controls for what we INCLUDE
#  on the right-hand side.  If an important confounder is left out,
#  we get omitted variable bias.  That is the topic of Section 2.


# =============================================================================
# SECTION 2 — Omitted Variable Bias
# =============================================================================
#
#  We now turn to a different dataset — California school districts —
#
#  The question: does reducing CLASS SIZE (student-teacher ratio)
#  improve TEST SCORES?
#
#  In the STAR experiment (Lab 1), this was straightforward — class
#  size was randomly assigned.  Here, class size is observational.
#  Wealthier districts can afford more teachers AND their students
#  score higher for many reasons unrelated to class size.
#
#  The key omitted variable: the percentage of students qualifying for
#  FREE OR SUBSIDISED MEALS (a direct measure of student poverty).
#
#  Reference: Stock, J.H. & Watson, M.W. (2007). Introduction to
#  Econometrics. The CASchools data feature extensively in their text.


# --- 2a. Load and explore the data ---

data("CASchools")

ca <- CASchools %>%
  mutate(
    testscr  = (read + math) / 2,       # average test score
    str      = students / teachers,      # student-teacher ratio
    meal_pct = lunch,                    # % free meals (already a %)
    el_pct   = english,                  # % English learners (already a %)
    avginc   = income                    # district avg income ($1000s)
  )

cat("Number of districts:", nrow(ca), "\n\n")

ca %>%
  select(testscr, str, meal_pct, el_pct, avginc) %>%
  as.data.frame() %>%
  stargazer(type = "text",
            title = "Summary Statistics — California School Districts",
            covariate.labels = c("Test Score", "Student-Teacher Ratio",
                                 "% Free Meals", "% English Learners",
                                 "Avg Income ($1000s)"),
            digits = 1)


# --- 2b. The short regression (omitting poverty) ---

reg_short <- lm(testscr ~ str, data = ca)

# --- 2c. The long regression (including poverty) ---

reg_long <- lm(testscr ~ str + meal_pct, data = ca)

# --- 2d. Compare short and long regressions ---

stargazer(reg_short, reg_long,
          type = "text",
          title = "Test Scores and Class Size: Short vs. Long Regression",
          column.labels = c("Short (OVB)", "Long (with poverty)"),
          dep.var.labels = "Average Test Score",
          covariate.labels = c("Student-Teacher Ratio", "% Free Meals"),
          omit.stat = c("f", "ser"),
          notes = c("Short regression omits % free meals (poverty proxy).",
                    "Adding it reduces the STR coefficient substantially."))

#  Look at the STR coefficient: it shrinks dramatically when we add
#  the poverty control.  The short regression overestimates the
#  (negative) effect of class size.

beta_short <- coef(reg_short)["str"]
beta_long  <- coef(reg_long)["str"]
ovb_actual <- beta_short - beta_long

cat("\nbeta_short (STR):", round(beta_short, 4), "\n")
cat("beta_long  (STR):", round(beta_long, 4),  "\n")
cat("OVB (actual):    ", round(ovb_actual, 4), "\n")


# --- 2e. Verify the OVB formula ---
#
#  The OVB formula says:
#
#     OVB = pi_1 * gamma
#
#  where:
#     pi_1  = coefficient from regressing the omitted variable (meal_pct)
#             on the explanatory variable (STR)
#     gamma = coefficient on the omitted variable (meal_pct) in the
#             long regression
#
#  Let's check this.

# Step 1: Regress the omitted variable on the explanatory variable
aux_reg <- lm(meal_pct ~ str, data = ca)
pi_1    <- coef(aux_reg)["str"]

cat("\n--- OVB Formula Verification ---\n")
cat("pi_1 (meal_pct ~ str):", round(pi_1, 4), "\n")

#  pi_1 > 0: districts with higher STR have more students on free meals.
#  This makes sense — poorer districts have larger classes.

# Step 2: Get gamma from the long regression
gamma_hat <- coef(reg_long)["meal_pct"]
cat("gamma (meal_pct in long reg):", round(gamma_hat, 4), "\n")

#  gamma < 0: higher poverty is associated with lower test scores,
#  even controlling for class size.

# Step 3: Compute predicted OVB
ovb_formula <- pi_1 * gamma_hat
cat("\nOVB (formula: pi_1 * gamma):", round(ovb_formula, 4), "\n")
cat("OVB (actual: short - long): ", round(ovb_actual, 4), "\n")
cat("Match?", abs(ovb_formula - ovb_actual) < 0.001, "\n")

#  The two numbers should be (nearly) identical.  This is not a
#  coincidence — it is a mathematical identity that always holds
#  for OLS.


# --- 2f. Predicting the direction of bias ---
#
#  Before running the regressions, we could have predicted the
#  direction of OVB using the sign table from the lecture slides:
#
#     OVB = pi_1 * gamma
#
#     pi_1 > 0   (higher STR -> more poverty in the district)
#     gamma < 0  (more poverty -> lower test scores)
#
#     => OVB < 0  (NEGATIVE BIAS — the short regression makes the
#                   STR effect look MORE NEGATIVE than it truly is)
#
#  In other words, the naive regression OVERESTIMATES the harm of
#  large classes.  Part of what looks like a "class size effect" is
#  actually a "poverty effect" absorbed into the STR coefficient.

cat("\n--- Bias Direction ---\n")
cat("Sign of pi_1: ", ifelse(pi_1 > 0, "POSITIVE", "NEGATIVE"),
    "(higher STR -> more poverty)\n")
cat("Sign of gamma:", ifelse(gamma_hat > 0, "POSITIVE", "NEGATIVE"),
    "(more poverty -> lower scores)\n")
cat("=> Bias is:   ", ifelse(ovb_formula > 0, "POSITIVE (upward)",
                              "NEGATIVE (downward)"), "\n")
cat("\nThe short regression exaggerates the negative effect of class size.\n")


# --- 2g. Adding more controls ---
#
#  Let's progressively add controls to see how the STR coefficient
#  changes.  This is the standard approach in applied economics:
#  show that the estimate is robust (or not) to adding covariates.

reg_1 <- lm(testscr ~ str, data = ca)
reg_2 <- lm(testscr ~ str + meal_pct, data = ca)
reg_3 <- lm(testscr ~ str + meal_pct + el_pct, data = ca)
reg_4 <- lm(testscr ~ str + meal_pct + el_pct + avginc, data = ca)

stargazer(reg_1, reg_2, reg_3, reg_4,
          type = "text",
          title = "Test Scores and Class Size: Progressive Controls",
          column.labels = c("Naive", "+ Poverty", "+ English L.",
                            "+ Income"),
          dep.var.labels = "Average Test Score",
          covariate.labels = c("Student-Teacher Ratio", "% Free Meals",
                               "% English Learners", "Avg Income ($1000s)"),
          omit.stat = c("f", "ser"),
          notes = c("Each column adds one more control variable.",
                    "Watch how the STR coefficient changes."))

#  QUESTION: What happens to the STR coefficient as we add controls?
#  Does it stabilise?  What does the final estimate suggest about the
#  causal effect of class size?

# --- 2h. Visualising OVB ---
#
#  Districts with high poverty (red) tend to have both high STR and
#  low test scores — creating a spurious negative correlation.

ca <- ca %>%
  mutate(poverty_group = ifelse(meal_pct > median(meal_pct),
                                "High Poverty", "Low Poverty"))

ggplot(ca, aes(x = str, y = testscr, colour = poverty_group)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", se = FALSE, linewidth = 1) +
  labs(
    title    = "Test Scores vs. STR, by Poverty Level",
    subtitle = "Within each group the slope is flatter than the overall relationship",
    x        = "Student-Teacher Ratio",
    y        = "Average Test Score",
    colour   = NULL
  ) +
  theme_minimal() +
  theme(legend.position = "bottom")

#  The overall relationship (mixing both groups) is steeper than
#  either within-group slope.  That extra steepness IS the OVB.


# =============================================================================
# SECTION 3 — Simultaneity: When Causation Runs Both Ways
# =============================================================================
#
#  The second major source of endogeneity is SIMULTANEITY (also called
#  reverse causality).  This occurs when the outcome and the explanatory
#  variable are determined at the same time.
#
#  The classic example from the lecture slides: the effect of POLICE
#  on CRIME.
#
#     - Does more police reduce crime?  (The causal channel we want)
#     - Does more crime attract more police?  (The reverse channel)
#
#  Both are true simultaneously.  A naive OLS regression of crime on
#  police will mix the two channels and can produce a POSITIVE coefficient
#  — making it look like more police CAUSES more crime, when in reality
#  police are simply deployed to high-crime areas.
#
#  We SIMULATE this data so we know the true causal effect and can see
#  exactly how OLS fails.


# --- 3a. The structural model ---
#
#  We have two simultaneous equations:
#
#     crime_i  = alpha_1 * police_i + beta_1 * poverty_i + mu_1
#     police_i = alpha_2 * crime_i  + beta_2 * budget_i  + mu_2
#
#  True structural parameters:
#     alpha_1 = -0.5   (more police REDUCES crime — the causal effect)
#     alpha_2 =  0.8   (more crime leads to more police deployment)
#     beta_1  =  1.0   (poverty increases crime)
#     beta_2  =  0.6   (larger budget increases police)
#
#  The exogenous variables (poverty and budget) are determined OUTSIDE
#  the system.  The endogenous variables (crime and police) are
#  determined INSIDE the system — they affect each other.

set.seed(446)
n <- 1000

# True structural parameters
alpha_1 <- -0.5    # police -> crime (the causal effect we want)
alpha_2 <-  0.8    # crime -> police (the reverse channel)
beta_1  <-  1.0    # poverty -> crime
beta_2  <-  0.6    # budget -> police

# Exogenous variables
poverty <- rnorm(n, mean = 50, sd = 10)
budget  <- rnorm(n, mean = 40, sd = 8)

# Structural shocks
mu_1 <- rnorm(n, sd = 5)
mu_2 <- rnorm(n, sd = 5)

# Solve the simultaneous system for the equilibrium values.
# From the two equations:
#   crime  = alpha_1 * police + beta_1 * poverty + mu_1
#   police = alpha_2 * crime  + beta_2 * budget  + mu_2
#
# Substituting and solving (as shown in the lecture slides):
#   crime  = [alpha_1*(beta_2*budget + mu_2) + beta_1*poverty + mu_1] /
#            (1 - alpha_1*alpha_2)
#   police = [alpha_2*(beta_1*poverty + mu_1) + beta_2*budget + mu_2] /
#            (1 - alpha_1*alpha_2)

denom <- 1 - alpha_1 * alpha_2

crime  <- (alpha_1 * (beta_2 * budget + mu_2) + beta_1 * poverty + mu_1) / denom
police <- (alpha_2 * (beta_1 * poverty + mu_1) + beta_2 * budget + mu_2) / denom

sim_police <- tibble(crime, police, poverty, budget)

cat("True causal effect of police on crime (alpha_1):", alpha_1, "\n")
cat("Reverse effect of crime on police (alpha_2):    ", alpha_2, "\n")
cat("Observed correlation(police, crime):             ",
    round(cor(police, crime), 3), "\n")


# --- 3b. The naive OLS regression ---
#
#  A researcher who does not account for simultaneity might just regress
#  crime on police:

naive_reg <- lm(crime ~ police, data = sim_police)

cat("\n--- Naive OLS: Crime ~ Police ---\n")
summary(naive_reg)

#  QUESTION: What sign does the coefficient have?  Is it positive or
#  negative?  Does it match the TRUE causal effect of -0.5?
#
#  If the coefficient is positive, OLS is telling us that more police
#  is associated with MORE crime.  A naive interpretation would be:
#  "police cause crime."  That is clearly wrong.
#
#  What went wrong?  Police and crime are determined simultaneously.
#  Cities with high crime deploy more police (alpha_2 > 0), creating
#  a positive correlation that overwhelms the negative causal effect.


# --- 3c. Adding poverty as a control ---
#
#  Does adding poverty help?

ctrl_reg <- lm(crime ~ police + poverty, data = sim_police)

stargazer(naive_reg, ctrl_reg,
          type = "text",
          title = "Crime and Police: Naive OLS",
          column.labels = c("No Controls", "Controlling for Poverty"),
          dep.var.labels = "Crime Rate",
          covariate.labels = c("Police", "Poverty"),
          omit.stat = c("f", "ser"),
          notes = c("True causal effect of police on crime = -0.5.",
                    "Simultaneity biases OLS regardless of controls."))

#  Even with the control, the police coefficient remains biased.
#  Controls help with omitted variable bias, but they CANNOT fix
#  simultaneity — the problem is that police and crime are in a
#  feedback loop.
#
#  QUESTION: Why can't adding controls solve the simultaneity problem?
#  (Hint: think about what is in the error term of the crime equation.
#  Even after controlling for poverty, the error mu_1 still feeds
#  into the police equation via the simultaneous system.)


# --- 3d. Visualising the simultaneity problem ---

ggplot(sim_police, aes(x = police, y = crime)) +
  geom_point(aes(colour = poverty), alpha = 0.4, size = 1.5) +
  geom_smooth(method = "lm", se = FALSE, colour = "red",
              linewidth = 1.2, linetype = "dashed") +
  geom_abline(intercept = mean(crime) - alpha_1 * mean(police),
              slope = alpha_1,
              colour = "darkgreen", linewidth = 1.2) +
  scale_colour_viridis_c(name = "Poverty") +
  labs(
    title    = "Police vs. Crime",
    subtitle = "Red dashed = naive OLS (biased); Green = true causal effect",
    x        = "Police Deployment",
    y        = "Crime Rate"
  ) +
  theme_minimal()

#  The green line shows the true causal relationship (negative slope).
#  The red line shows what OLS estimates (positive or less negative).
#  The divergence is caused by simultaneity: high-crime areas get more
#  police, pulling the estimated slope upward.


# --- 3e. What would we need to fix this? ---
#
#  Simultaneity cannot be solved by adding controls.  We need a source
#  of variation in police that is NOT driven by crime.  In the language
#  of econometrics, we need an INSTRUMENTAL VARIABLE — something that
#  shifts police deployment for reasons unrelated to crime.
#
#  In our simulation, BUDGET is such a variable: it affects police
#  (higher budget -> more police) but does not directly affect crime
#  (except through police).
#
#  We will study instrumental variables in a later lab.  For now, the
#  key lesson is: KNOW YOUR ENDOGENEITY PROBLEM.  Is it omitted
#  variables?  Simultaneity?  The solution depends on the diagnosis.

# =============================================================================
# End of Lab 2
# =============================================================================
