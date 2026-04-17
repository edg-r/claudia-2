# =============================================================================
#  GPEC 446 — Lab 1: Introduction to Causal Inference
#  The Tennessee STAR Experiment
#  David L. Vargas
#  Last modified: 04.02.2026
# =============================================================================
#
#  In this lab we use data from the Tennessee STAR experiment to learn three
#  foundational ideas in causal inference:
#
#    1. The selection problem — why naive comparisons can be misleading
#    2. Random assignment as a solution
#    3. How to estimate and interpret treatment effects
#
#  The structure follows Angrist & Pischke, Mastering 'Metrics, Ch. 1.
#
#  Data: Project STAR (Student/Teacher Achievement Ratio), available in the
#        AER package for R.
#
# =============================================================================


# -----------------------------------------------------------------------------
# SECTION 1 — The Policy Question and the Selection Problem
# -----------------------------------------------------------------------------
#
#  Does reducing class size improve student achievement?
#
#  This seems like it should be easy to answer: just compare test scores in
#  small classes vs. large classes. But there is a problem.
#
#  Think about which students end up in small classes in practice.  Their
#  parents may live in wealthier districts, may be more involved in their
#  children's education, or may have actively sought out schools with small
#  classes.  These families differ from the average family in many ways that
#  also affect test scores.
#
#  So if we see that students in small classes score higher, we cannot tell
#  whether the difference is due to:
#     (a) the small class itself, or
#     (b) all the other advantages those students already had.
#
#  This is the SELECTION PROBLEM: the "treatment" (small class) is not
#  assigned at random — people select into it, and that selection is
#  correlated with the outcome.
#
#  How can we solve this?  Run an experiment.
#
#  In the mid-1980s, Tennessee randomly assigned over 11,000 students
#  entering kindergarten to one of three types of classrooms:
#
#     - Small class        (13-17 students per teacher)
#     - Regular class      (22-25 students per teacher)
#     - Regular + aide     (22-25 students with a full-time teacher's aide)
#
#  Because assignment was random, students in each group should be similar
#  on average in every dimension — family income, parental education,
#  motivation — whether we observe those things or not.
#
#  Any difference in outcomes can therefore be attributed to class size.
#  That is the power of randomisation.
#


# -----------------------------------------------------------------------------
# SECTION 2 — Load and Explore the Data
# -----------------------------------------------------------------------------

# Install packages if you haven't already (uncomment the lines below):
# install.packages("AER")
# install.packages("tidyverse")
# install.packages("stargazer")

library(AER)
library(tidyverse)
library(stargazer)

# Load the STAR dataset
data("STAR")

# How big is the dataset?
dim(STAR)          # rows = students, columns = variables

# What variables do we have?
names(STAR)

# The dataset follows students from kindergarten (K) through 3rd grade.
# Today we focus on KINDERGARTEN only, since that is when students were
# first randomly assigned.
#
# Key variables for kindergarten:
#   stark     — treatment group in K: "small", "regular", "regular+aide"
#   readk     — reading scaled score in K
#   mathk     — math scaled score in K
#   lunchk    — free lunch status in K (proxy for family income)
#   schoolk   — school type: "inner-city", "suburban", "rural", "urban"
#   ethnicity — student race/ethnicity
#   gender    — "male" or "female"

# Quick look at the treatment variable
# (useNA = "ifany" shows NA count — not all students have K data)
table(STAR$stark, useNA = "ifany")

# --- Create a clean kindergarten-only dataset using tidyverse ---

star_k <- STAR %>%
  filter(!is.na(stark)) %>%                     # keep only K participants
  select(stark, mathk, readk, lunchk, schoolk,  # select the variables we need
         ethnicity, gender) %>%
  mutate(                                        # create indicator variables
    free_lunch = as.numeric(lunchk == "free", na.rm = TRUE),
    white      = as.numeric(ethnicity == "cauc", na.rm = TRUE),
    afam       = as.numeric(ethnicity == "afam", na.rm = TRUE),
    female     = as.numeric(gender == "female", na.rm = TRUE),
    inner_city = as.numeric(schoolk == "inner-city", na.rm = TRUE)
  )

# How many students?  How are they split across treatment arms?
star_k %>% count(stark)

# What share in each arm?
star_k %>% count(stark) %>% mutate(share = n / sum(n))

# Quick summary statistics using stargazer
# stargazer can summarise data frames too — not just regressions!
# We select only the numeric columns we care about.

star_k %>%
  select(mathk, readk, free_lunch, white, afam, female, inner_city) %>%
  as.data.frame() %>%
  stargazer(type = "text",
            title = "Summary Statistics — Kindergarten Sample",
            digits = 2)


# -----------------------------------------------------------------------------
# SECTION 3 — The Balance Table
# -----------------------------------------------------------------------------
#
#  If randomisation worked, the three groups should look similar in terms
#  of their baseline characteristics.  A BALANCE TABLE checks this by
#  comparing the average of each covariate across treatment arms.
#
#  This is the analog of Table 1.3 in Mastering 'Metrics.
#
#  Why does this matter?  If the groups look different on observables,
#  we would worry that they also differ on unobservables — and then any
#  difference in test scores might not be causal.


# --- 3a. Summary statistics by treatment arm using stargazer ---
#
#  We use stargazer to produce a clean summary table for each treatment
#  group separately.  This lets us eyeball whether the groups look
#  similar — exactly like Table 1.3 in Mastering 'Metrics.

# Select the covariates we want to compare
balance_vars <- c("free_lunch", "white", "afam", "female", "inner_city")

# Summary stats for the SMALL CLASS group
cat("\n===== SMALL CLASS =====\n")
star_k %>%
  filter(stark == "small") %>%
  select(all_of(balance_vars)) %>%
  as.data.frame() %>%
  stargazer(type = "text", digits = 3,
            title = "Small Class",
            covariate.labels = c("Free Lunch", "White", "African-American",
                                 "Female", "Inner-City School"))

# Summary stats for the REGULAR CLASS group
cat("\n===== REGULAR CLASS =====\n")
star_k %>%
  filter(stark == "regular") %>%
  select(all_of(balance_vars)) %>%
  as.data.frame() %>%
  stargazer(type = "text", digits = 3,
            title = "Regular Class",
            covariate.labels = c("Free Lunch", "White", "African-American",
                                 "Female", "Inner-City School"))

# Summary stats for the REGULAR + AIDE group
cat("\n===== REGULAR + AIDE =====\n")
star_k %>%
  filter(stark == "regular+aide") %>%
  select(all_of(balance_vars)) %>%
  as.data.frame() %>%
  stargazer(type = "text", digits = 3,
            title = "Regular + Aide",
            covariate.labels = c("Free Lunch", "White", "African-American",
                                 "Female", "Inner-City School"))

#  Compare the "Mean" column across the three tables.
#  Do the groups look similar?  They should — that is what
#  randomisation buys us.


# --- 3b. Test for statistically significant differences ---
#
#  For each covariate, we test whether the mean differs between the
#  "small" and "regular" groups using a t-test.
#
#  We do this one variable at a time so you can see exactly what is
#  happening at each step.

# First, split the data into the two groups we want to compare
small   <- star_k %>% filter(stark == "small")
regular <- star_k %>% filter(stark == "regular")

# Test 1: Free lunch
t.test(small$free_lunch, regular$free_lunch)

# Test 2: White
t.test(small$white, regular$white)

# Test 3: African-American
t.test(small$afam, regular$afam)

# Test 4: Female
t.test(small$female, regular$female)

# Test 5: Inner-city school
t.test(small$inner_city, regular$inner_city)

#  QUESTION: Do you see any large or statistically significant differences?
#  If one or two covariates show p < 0.05, is that evidence that
#  randomisation failed?  (Hint: with 5 tests at the 5% level, how many
#  significant results would you expect by chance alone?)


# --- 3c. Combined balance table (approach 1: means + t-tests with kable) ---
#
#  Let's collect everything we just did into a single, clean table.
#  We compute group means by hand, differences, and p-values from the
#  t-tests, then display with kable() for a nice formatted output.
#
#  This is the most transparent approach: you can see exactly where
#  every number comes from.

# install.packages("knitr")    # uncomment if needed
library(knitr)

# Also get the regular+aide group
reg_aide <- star_k %>% filter(stark == "regular+aide")

balance_summary <- tibble(
  Variable = c("Free Lunch", "White", "African-American",
               "Female", "Inner-City School"),

  # Group means — computed one at a time
  Small = c(mean(small$free_lunch, na.rm = TRUE),
            mean(small$white,      na.rm = TRUE),
            mean(small$afam,       na.rm = TRUE),
            mean(small$female,     na.rm = TRUE),
            mean(small$inner_city, na.rm = TRUE)),

  Regular = c(mean(regular$free_lunch, na.rm = TRUE),
              mean(regular$white,      na.rm = TRUE),
              mean(regular$afam,       na.rm = TRUE),
              mean(regular$female,     na.rm = TRUE),
              mean(regular$inner_city, na.rm = TRUE)),

  `Reg + Aide` = c(mean(reg_aide$free_lunch, na.rm = TRUE),
                   mean(reg_aide$white,      na.rm = TRUE),
                   mean(reg_aide$afam,       na.rm = TRUE),
                   mean(reg_aide$female,     na.rm = TRUE),
                   mean(reg_aide$inner_city, na.rm = TRUE)),

  # Difference = Small minus Regular
  Difference = c(mean(small$free_lunch, na.rm = TRUE) - mean(regular$free_lunch, na.rm = TRUE),
                 mean(small$white,      na.rm = TRUE) - mean(regular$white,      na.rm = TRUE),
                 mean(small$afam,       na.rm = TRUE) - mean(regular$afam,       na.rm = TRUE),
                 mean(small$female,     na.rm = TRUE) - mean(regular$female,     na.rm = TRUE),
                 mean(small$inner_city, na.rm = TRUE) - mean(regular$inner_city, na.rm = TRUE)),

  # p-values from the t-tests we already ran
  `p-value` = c(t.test(small$free_lunch, regular$free_lunch)$p.value,
                t.test(small$white,      regular$white)$p.value,
                t.test(small$afam,       regular$afam)$p.value,
                t.test(small$female,     regular$female)$p.value,
                t.test(small$inner_city, regular$inner_city)$p.value)
)

# Print with kable for a clean, aligned table
balance_summary %>%
  mutate(across(where(is.numeric), ~ round(.x, 3))) %>%
  kable(align = c("l", "r", "r", "r", "r", "r"),
        caption = "Balance Table: Covariate Means by Treatment Arm")

#  Read this table:
#    - The first three columns show group means
#    - "Difference" = Small minus Regular
#    - "p-value" = from a two-sample t-test of Small vs. Regular
#
#  If randomisation worked, the "Difference" column should be close to zero
#  and the p-values should mostly be large (> 0.05).


# --- 3d. The same table using regressions + stargazer ---
#
#  Here is a trick commonly used in economics papers to make the same
#  balance table.  The idea: run a regression of EACH COVARIATE on the
#  treatment indicator.
#
#     covariate_i = beta_0 + beta_1 * SmallClass + error
#
#  In this regression:
#     beta_0 (intercept) = mean of the covariate in the regular group
#     beta_1 (slope)     = difference in means (small minus regular)
#
#  This works because with a single binary regressor, OLS = difference
#  in means.  (We will see why in Section 4!)
#
#  The advantage: stargazer formats everything into a publication-ready
#  table automatically — coefficients, standard errors, and significance
#  stars all in one place.

# First, create explicit dummy variables for each treatment arm.
# A "dummy" (or indicator) is a variable that equals 1 if the student
# belongs to that group, and 0 otherwise.

star_k <- star_k %>%
  mutate(
    small    = as.numeric(stark == "small"),
    reg_aide = as.numeric(stark == "regular+aide")
  )

# Check that the dummies make sense
star_k %>% count(stark, small, reg_aide)

#  Notice we did NOT create a dummy for "regular".  With three groups, we
#  only need two dummies — the third group (regular) is the REFERENCE
#  category, captured by the intercept.  This avoids perfect collinearity
#  (the "dummy variable trap").

# Now run the balance regressions using the dummies we created.
# Each regression asks: does the covariate differ across groups?
#
#   covariate_i = beta_0 + beta_1 * small + beta_2 * reg_aide + error
#
#   beta_0 = mean for the regular group (the reference)
#   beta_1 = difference: small minus regular
#   beta_2 = difference: regular+aide minus regular

bal_free_lunch <- lm(free_lunch ~ small + reg_aide, data = star_k)
bal_white      <- lm(white      ~ small + reg_aide, data = star_k)
bal_afam       <- lm(afam       ~ small + reg_aide, data = star_k)
bal_female     <- lm(female     ~ small + reg_aide, data = star_k)
bal_inner_city <- lm(inner_city ~ small + reg_aide, data = star_k)

# Now stargazer puts it all in one table
stargazer(bal_free_lunch, bal_white, bal_afam, bal_female, bal_inner_city,
          type = "text",
          title = "Balance Table (Kindergarten)",
          column.labels = c("Free Lunch", "White", "Afr-Am",
                            "Female", "Inner-City"),
          covariate.labels = c("Small Class", "Regular + Aide"),
          dep.var.labels.include = FALSE,
          model.numbers = FALSE,
          omit.stat = c("f", "ser", "adj.rsq"),
          notes = c("Each column is a separate OLS regression of the covariate",
                    "on treatment dummies. Intercept = regular class mean.",
                    "Standard errors in parentheses."))

#  Compare the two tables (kable vs. stargazer).  The numbers should match!
#    - The "Intercept" row in stargazer = the "Regular" column in kable
#    - The "Small Class" row in stargazer = the "Difference" column in kable
#    - The stars in stargazer correspond to the p-values in kable
#
#  The stargazer version is more compact and closer to what you see in
#  published papers.  The kable version is easier to read and customize.
#  Both are valid ways to present a balance table.


# -----------------------------------------------------------------------------
# SECTION 4 — Estimating the Treatment Effect
# -----------------------------------------------------------------------------
#
#  Now the payoff.  We want to estimate the CAUSAL EFFECT of being in a
#  small class on kindergarten math scores.
#
#  Under random assignment, the simplest estimator is the
#  DIFFERENCE IN MEANS between treated and control groups.


# --- 4a. Difference in means ---

# For clarity, let's compare just two groups: small vs. regular.
# (We set aside the "regular+aide" group for now.)

star_sr <- star_k %>%
  filter(stark %in% c("small", "regular")) %>%
  mutate(stark = droplevels(stark))          # drop unused factor level

# Compute group means
star_sr %>%
  group_by(stark) %>%
  summarise(
    n         = n(),
    math_mean = mean(mathk, na.rm = TRUE),
    math_sd   = sd(mathk, na.rm = TRUE)
  )

# The difference
means <- star_sr %>%
  group_by(stark) %>%
  summarise(math_mean = mean(mathk, na.rm = TRUE))

diff_in_means <- means$math_mean[means$stark == "small"] -
                 means$math_mean[means$stark == "regular"]

cat("Difference in means (small - regular):", round(diff_in_means, 2), "\n")

# Is this difference statistically significant?
t.test(mathk ~ stark, data = star_sr)


# --- 4b. The same estimate via regression ---
#
#  A linear regression of the outcome on a treatment indicator gives us
#  the exact same difference in means — plus standard errors, p-values,
#  and a framework we can build on in future weeks.

reg1 <- lm(mathk ~ stark, data = star_sr)
summary(reg1)

#  The coefficient on "starksmall" IS the difference in means:
cat("\nDifference in means:   ", round(diff_in_means, 2), "\n")
cat("Regression coefficient:", round(coef(reg1)["starksmall"], 2), "\n")

#  QUESTION: Why are these two numbers the same?  What is the regression
#  doing when the only right-hand-side variable is a binary indicator?


# --- 4c. Adding covariates ---
#
#  With a well-run experiment, adding controls should not change the
#  treatment effect much — randomisation already made the groups comparable.
#  But controls can reduce residual variance and make the estimate more
#  PRECISE (smaller standard errors).

reg2 <- lm(mathk ~ stark + free_lunch + white + female, data = star_sr)

# Compare the two models side by side using stargazer.
# stargazer() produces clean regression tables — the same format you see
# in published economics papers.
#
# type = "text" prints to the console.  Change to "html" or "latex" if
# you want to export a table for a paper or presentation.

stargazer(reg1, reg2,
          type = "text",
          title = "Effect of Small Class on Math Scores (Kindergarten)",
          column.labels = c("No Controls", "With Controls"),
          dep.var.labels = "Math Score (K)",
          covariate.labels = c("Small Class", "Free Lunch",
                               "White", "Female"),
          omit.stat = c("f", "ser"),
          notes = "Data: Project STAR. OLS estimates.")

#  QUESTION: Did adding covariates change the point estimate much?
#  Did it change the standard error?  Why does this pattern make sense
#  in a randomised experiment?


# --- 4d. Now try it for reading scores ---

# YOUR TURN: repeat the analysis above using readk instead of mathk.
# Uncomment and fill in the blanks:

# reg_read1 <- lm(_____ ~ stark, data = star_sr)
# reg_read2 <- lm(_____ ~ stark + free_lunch + white + female, data = star_sr)
#
# stargazer(reg_read1, reg_read2,
#           type = "text",
#           column.labels = c("No Controls", "With Controls"),
#           dep.var.labels = "Reading Score (K)",
#           covariate.labels = c("Small Class", "Free Lunch",
#                                "White", "Female"),
#           omit.stat = c("f", "ser"))


# --- 4e. Bringing in the third arm ---
#
#  So far we compared small vs. regular.  What about "regular+aide"?
#  Let's use the full sample with all three arms.

reg_all <- lm(mathk ~ stark, data = star_k)

stargazer(reg_all,
          type = "text",
          title = "Effect of Class Type on Math Scores (All Three Arms)",
          dep.var.labels = "Math Score (K)",
          covariate.labels = c("Small Class", "Regular + Aide"),
          omit.stat = c("f", "ser"),
          notes = "Reference category: Regular class.")

#  QUESTION: Does adding a teacher's aide seem to help as much as
#  reducing class size?  What might explain this?


# -----------------------------------------------------------------------------
# SECTION 5 — What Have We Learned?
# -----------------------------------------------------------------------------

# --- Effect size in standard deviation units ---

sd_math <- sd(star_sr$mathk, na.rm = TRUE)
effect  <- coef(reg1)["starksmall"]

cat("Treatment effect:       ", round(effect, 2), "points\n")
cat("SD of math scores:      ", round(sd_math, 2), "points\n")
cat("Effect size (Cohen's d):", round(effect / sd_math, 2), "SD\n")

#  An effect of roughly 0.2 standard deviations is considered a "small to
#  medium" effect in education research — but in a policy context, it is
#  meaningful, especially because it comes from a single, well-defined
#  intervention.


# --- A quick visualisation ---

star_sr %>%
  filter(!is.na(mathk)) %>%
  ggplot(aes(x = mathk, fill = stark)) +
  geom_density(alpha = 0.4) +
  labs(
    title = "Distribution of Kindergarten Math Scores by Class Type",
    x     = "Math Scaled Score",
    y     = "Density",
    fill  = "Class Type"
  ) +
  theme_minimal()


# --- Key Takeaways ---
#
#  1. The SELECTION PROBLEM makes it hard to learn causal effects from
#     observational data.  Students who end up in small classes are
#     different from those in large classes in ways that also affect
#     test scores.
#
#  2. RANDOM ASSIGNMENT solves the selection problem.  It makes treatment
#     and control groups comparable on average — on both observed and
#     unobserved characteristics.
#
#  3. We check that randomisation "worked" by building a BALANCE TABLE.
#     If the groups look similar on observables, we are more confident
#     they are also similar on unobservables.
#
#  4. The treatment effect can be estimated as a simple DIFFERENCE IN MEANS
#     or equivalently as a REGRESSION COEFFICIENT.  Adding controls to the
#     regression should not change the point estimate much (because groups
#     are already balanced) but can improve precision.
#
#
# =============================================================================
# End of Lab 1
# =============================================================================
