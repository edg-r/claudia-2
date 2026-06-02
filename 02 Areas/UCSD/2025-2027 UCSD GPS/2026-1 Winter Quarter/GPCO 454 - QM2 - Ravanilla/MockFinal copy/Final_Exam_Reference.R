# ============================================================================
# QM2 FINAL EXAM — PLUG-AND-PLAY R REFERENCE SHEET
# Name: Edgar Agunias
# ============================================================================
# HOW TO USE THIS FILE:
#   1. Copy the whole file into a new R script at the start of the exam.
#   2. Fill in the blanks marked with <___> (variable names, file names, etc.).
#   3. Delete any sections you don't need.
#   4. Each section is self-contained — you can run them in order top to bottom.
# ============================================================================


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 1: SETUP — Packages, Working Directory, Load Data             ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# Set your working directory to wherever the exam data lives
setwd("<your_folder_path>")  # e.g., setwd("~/Desktop/Final")
getwd()                       # Confirm it's correct

# Load all packages you might need (install first if not already installed)
library(tidyverse)      # dplyr, ggplot2, tidyr, etc. — data wrangling + plotting
library(readxl)         # read_excel() for .xlsx files
library(stargazer)      # Formatted regression tables
library(ggplot2)        # Plotting (also loaded by tidyverse, but explicit is fine)
library(car)            # vif() for multicollinearity, avPlots()
library(lmtest)         # bptest() for Breusch-Pagan heteroskedasticity test
library(sandwich)       # vcovHC() for robust standard errors
library(interactions)   # interaction plots (if needed)
library(ggeffects)      # ggpredict() for interaction marginal effects plots

# --- Load the exam data ---
data <- read_excel("part2_final_exam_simulation_data_final.xlsx", sheet = "simulation_data")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  DATASET QUICK REFERENCE (174 countries, 9 variables):                  │
# │                                                                         │
# │  entity                               → Country name (character)        │
# │  ti-corruption-perception-index-2018   → Corruption perception (higher  │
# │                                          = less corrupt, 0–100)         │
# │  liberal-democracy                     → Binary: 1 = liberal democracy  │
# │  gdp-per-capita-worldbank-2020         → GDP per capita in USD          │
# │  democracy-index-eiu-2020              → Democracy index (0–10 scale)   │
# │  share-of-women-in-parliament-1990s    → % women in parliament (1990s)  │
# │  share-of-women-in-parliament-2010s    → % women in parliament (2010s)  │
# │  maternal-mortality-1990s              → Maternal mortality rate (1990s)│
# │  maternal-mortality-2010s              → Maternal mortality rate (2010s)│
# └─────────────────────────────────────────────────────────────────────────┘

# IMPORTANT: Column names have hyphens, so R won't accept them bare.
# Option A: Use backticks every time you reference them (annoying but works):
#   data$`ti-corruption-perception-index-2018`
# Option B (RECOMMENDED): Rename columns to clean R-friendly names right away:
data <- data %>%
  rename(
    country        = entity,
    corruption     = `ti-corruption-perception-index-2018`,
    liberal_dem    = `liberal-democracy`,
    gdp_pc         = `gdp-per-capita-worldbank-2020`,
    dem_index      = `democracy-index-eiu-2020`,
    women_parl_90s = `share-of-women-in-parliament-1990s`,
    women_parl_10s = `share-of-women-in-parliament-2010s`,
    mat_mort_90s   = `maternal-mortality-1990s`,
    mat_mort_10s   = `maternal-mortality-2010s`
  )

# For CSV files (if they switch format on you):
# data <- read.csv("<filename>.csv")

# For tab-delimited files:
# data <- read.table("<filename>.tab", header = TRUE, sep = "\t", encoding = "ISO-8859-1")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 2: INSPECT & UNDERSTAND THE DATA                                ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# Quick look at the data
head(data)               # First 6 rows
str(data)                # Column names, types, and sample values
summary(data)            # Descriptive statistics (min, max, mean, quartiles)
dim(data)                # Number of rows and columns
colnames(data)           # List all column names

# Check for missing values
sum(is.na(data))                    # Total NAs in the entire dataset
colSums(is.na(data))                # NAs per column

# Check unique values in a variable
length(unique(data$country))        # Should be 174 unique countries
table(data$liberal_dem)             # Frequency table: how many liberal democracies vs not

# Quick look at variable distributions
summary(data$corruption)
summary(data$gdp_pc)
summary(data$dem_index)
summary(data$mat_mort_10s)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 3: DATA CLEANING                                                ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# --- 3a. Replace non-numeric placeholders (e.g., "." or "(D)") with NA ---
# Use this when the data has string placeholders instead of actual missing values
# data <- data %>%
#   mutate(across(all_of(c("<col1>", "<col2>")),
#                 ~ ifelse(.x == ".", NA, .x)))

# --- 3b. Convert columns from character to numeric ---
# data <- data %>%
#   mutate(across(all_of(c("<col1>", "<col2>")), as.numeric))

# --- 3c. Remove rows with any NA values ---
data_clean <- data %>% na.omit()
# Or remove NAs only in specific columns:
# data_clean <- data %>% drop_na(corruption, gdp_pc)

# --- 3d. Create new variables using the EXAM DATA ---

# Change in women's parliamentary representation (1990s → 2010s):
data <- data %>%
  mutate(
    women_parl_change = women_parl_10s - women_parl_90s,
    women_parl_pct_change = ifelse(women_parl_90s != 0,
                                   100 * (women_parl_change / women_parl_90s),
                                   NA)
  )

# Change in maternal mortality (1990s → 2010s):
data <- data %>%
  mutate(
    mat_mort_change = mat_mort_10s - mat_mort_90s,
    mat_mort_pct_change = ifelse(mat_mort_90s != 0,
                                 100 * (mat_mort_change / mat_mort_90s),
                                 NA)
  )

# Log transformations (useful for right-skewed data like GDP and mortality):
data <- data %>%
  mutate(
    log_gdp_pc      = log(1 + gdp_pc),
    log_mat_mort_10s = log(1 + mat_mort_10s),
    log_mat_mort_90s = log(1 + mat_mort_90s)
  )
# NOTE: Use log(1 + x) when x can be 0. Don't log negative values.

# --- 3e. Create dummy / binary indicator variables ---
# liberal_dem is already binary (0/1) in the data.
# Example: create a "high corruption" dummy (above median):
data <- data %>%
  mutate(high_corruption = ifelse(corruption > median(corruption, na.rm = TRUE), 1, 0))

# --- 3f. Create categorical variables ---
data <- data %>%
  mutate(dem_category = case_when(
    dem_index < 4   ~ "Authoritarian",
    dem_index < 6   ~ "Hybrid",
    dem_index < 8   ~ "Flawed Democracy",
    dem_index >= 8  ~ "Full Democracy",
    TRUE            ~ NA_character_
  ))
# Convert to factor so R treats it as categorical in regressions:
data$dem_category <- factor(data$dem_category,
                            levels = c("Authoritarian", "Hybrid",
                                       "Flawed Democracy", "Full Democracy"))

# --- 3g. Filter / subset data ---
# Example: keep only democracies
# data_subset <- data %>% filter(liberal_dem == 1)
# Example: remove outliers
# data_subset <- data %>% filter(abs(gdp_pc) < some_threshold)

# --- REBUILD data_clean AFTER all transformations ---
data_clean <- data %>% na.omit()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 4: EXPLORATORY PLOTS                                            ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# --- 4a. Scatterplot with regression line ---
# Use this to visualize the relationship between your IV and DV
ggplot(data, aes(x = <IV>, y = <DV>)) +
  geom_point(size = 1, alpha = 0.75) +
  geom_smooth(method = "lm", se = TRUE, color = "red") +
  labs(
    title = "<Title>",
    x = "<X-axis label>",
    y = "<Y-axis label>"
  ) +
  theme_minimal()

# --- 4b. Histogram ---
# Use this to check the distribution of a single variable
ggplot(data, aes(x = <variable>)) +
  geom_histogram(bins = 30, fill = "skyblue", color = "black") +
  labs(
    title = "Distribution of <Variable>",
    x = "<Variable>",
    y = "Frequency"
  ) +
  theme_minimal()

# --- 4c. Boxplot ---
# Good for spotting outliers visually
ggplot(data, aes(x = "", y = <variable>)) +
  geom_boxplot(fill = "lightcoral", outlier.color = "red") +
  labs(title = "Boxplot of <Variable>", y = "<Variable>") +
  theme_minimal()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 5: REGRESSION ANALYSIS — Build Models Progressively             ║
# ╚══════════════════════════════════════════════════════════════════════════╝
# Strategy: Start with bivariate, then add controls one at a time.
# This lets you see how the main IV coefficient changes (OVB detection).

# ==========================================================================
# FILL IN YOUR CAUSAL QUESTION HERE:
# DV (outcome)    = <___>    e.g., mat_mort_10s, log_mat_mort_10s, women_parl_10s
# IV (treatment)  = <___>    e.g., corruption, liberal_dem, dem_index, gdp_pc
# Controls        = <___>    e.g., gdp_pc, dem_index, women_parl_90s, mat_mort_90s
# ==========================================================================

# --- Model 1: Bivariate (just IV and DV) ---
model1 <- lm(<DV> ~ <IV>, data = data_clean)

# --- Model 2: Add first control variable ---
model2 <- lm(<DV> ~ <IV> + <control_1>, data = data_clean)

# --- Model 3: Add more controls ---
model3 <- lm(<DV> ~ <IV> + <control_1> + <control_2>, data = data_clean)

# --- Model 4: Full model with all controls ---
model4 <- lm(<DV> ~ <IV> + <control_1> + <control_2> + <control_3>,
             data = data_clean)

# Quick look at any model's results:
summary(model4)

# ── EXAMPLE with this dataset (delete or adapt as needed) ──────────────
# Suppose the question is: "Does corruption affect maternal mortality?"
#   DV  = log_mat_mort_10s
#   IV  = corruption
#   Controls = gdp_pc, dem_index, women_parl_10s
#
# ex_m1 <- lm(log_mat_mort_10s ~ corruption, data = data_clean)
# ex_m2 <- lm(log_mat_mort_10s ~ corruption + log_gdp_pc, data = data_clean)
# ex_m3 <- lm(log_mat_mort_10s ~ corruption + log_gdp_pc + dem_index, data = data_clean)
# ex_m4 <- lm(log_mat_mort_10s ~ corruption + log_gdp_pc + dem_index + women_parl_10s, data = data_clean)
# ───────────────────────────────────────────────────────────────────────


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 6: REGRESSION TABLE — Stargazer Output                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# --- 6a. Basic stargazer table (no robust SEs) ---
stargazer(
  model1, model2, model3, model4,
  type = "text",                          # "text" for console, "html" for file
  title = "Regression Results",
  dep.var.labels = "<DV Label>",
  covariate.labels = c(
    "<IV Label>",
    "<Control 1 Label>",
    "<Control 2 Label>",
    "<Control 3 Label>"
  ),
  out = "regression_table.txt"            # saves to file
)

# --- 6b. Stargazer table WITH HC1 robust standard errors ---
# Calculate robust SEs for each model
robust_se <- list(
  sqrt(diag(vcovHC(model1, type = "HC1"))),
  sqrt(diag(vcovHC(model2, type = "HC1"))),
  sqrt(diag(vcovHC(model3, type = "HC1"))),
  sqrt(diag(vcovHC(model4, type = "HC1")))
)

# Calculate robust p-values for correct significance stars
robust_p <- list(
  coeftest(model1, vcov. = vcovHC(model1, type = "HC1"))[, 4],
  coeftest(model2, vcov. = vcovHC(model2, type = "HC1"))[, 4],
  coeftest(model3, vcov. = vcovHC(model3, type = "HC1"))[, 4],
  coeftest(model4, vcov. = vcovHC(model4, type = "HC1"))[, 4]
)

stargazer(
  model1, model2, model3, model4,
  type = "text",
  title = "Regression Results (Robust SEs)",
  dep.var.labels = "<DV Label>",
  covariate.labels = c(
    "<IV Label>",
    "<Control 1 Label>",
    "<Control 2 Label>",
    "<Control 3 Label>"
  ),
  se = robust_se,                          # plug in robust SEs
  p  = robust_p,                           # plug in robust p-values for stars
  omit.stat = c("f", "ser"),
  add.lines = list(
    c("Robust SEs", "HC1", "HC1", "HC1", "HC1")
  ),
  notes = "HC1 robust standard errors in parentheses.",
  out = "regression_table_robust.txt"
)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 7: GAUSS-MARKOV ASSUMPTION CHECKS                               ║
# ╚══════════════════════════════════════════════════════════════════════════╝
# Pick whichever model is your "final" model (usually the fullest one).
final_model <- model4   # <-- change this to whichever model you want to test

# -----------------------------------------------------------------------
# GM1: LINEARITY — Residuals vs. Fitted Values Plot
# -----------------------------------------------------------------------
# WHAT TO LOOK FOR: Random scatter around 0 with no curve or pattern.
# If you see a U-shape or clear curve → nonlinearity problem.

data_clean$residuals  <- final_model$residuals
data_clean$fittedvals <- final_model$fitted.values

# Check that mean of residuals is ~0 (it should be by construction)
mean(data_clean$residuals)

# Residuals vs. Fitted plot
ggplot(data_clean, aes(x = fittedvals, y = residuals)) +
  geom_point(alpha = 0.5) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
  labs(
    title = "Residuals vs. Fitted Values (Linearity Check)",
    x = "Fitted Values",
    y = "Residuals"
  ) +
  theme_minimal()

# OPTIONAL: If nonlinearity is detected, try adding a squared term:
# model_poly <- lm(<DV> ~ <IV> + I(<IV>^2) + <controls>, data = data_clean)

# Base R diagnostic plots (alternative — produces 4 standard plots):
# par(mfrow = c(2, 2))
# plot(final_model)
# par(mfrow = c(1, 1))

# -----------------------------------------------------------------------
# GM2: MULTICOLLINEARITY — Variance Inflation Factor (VIF)
# -----------------------------------------------------------------------
# INTERPRETATION:
#   VIF = 1       → no multicollinearity
#   VIF 1 to 5    → moderate (usually OK)
#   VIF > 10      → severe multicollinearity (problem!)
# FIX: Drop one of the highly correlated variables.

vif(final_model)

# -----------------------------------------------------------------------
# GM3: HETEROSKEDASTICITY — Breusch-Pagan & White Tests + Robust SEs
# -----------------------------------------------------------------------
# WHAT: Tests whether the variance of residuals is constant (homoskedastic).
# Null hypothesis (H0): Variance is constant (homoskedasticity).
# If p < 0.05 → reject H0 → heteroskedasticity is present.

# Breusch-Pagan test
bptest(final_model)

# White test (includes squared fitted values to catch nonlinear heteroskedasticity)
bptest(final_model, ~ fitted(final_model) + I(fitted(final_model)^2))

# FIX: Use HC1 robust standard errors (does NOT change coefficients, only SEs)
coeftest(final_model, vcov = vcovHC(final_model, type = "HC1"))

# -----------------------------------------------------------------------
# GM4: NON-RANDOM SAMPLING (qualitative — no R test)
# -----------------------------------------------------------------------
# Discuss in your write-up:
# - Is the sample representative of the population you're making claims about?
# - Selection bias? Convenience sample? Survivorship bias?
# - Affects EXTERNAL VALIDITY (generalizability of results).

# -----------------------------------------------------------------------
# GM5: ENDOGENEITY (qualitative — no single R test)
# -----------------------------------------------------------------------
# Discuss in your write-up — three main sources:
# 1. Omitted Variable Bias (OVB): Is there a variable correlated with both
#    the IV and DV that you haven't controlled for?
#    → Watch how the IV coefficient changes as you add controls.
# 2. Measurement Error: Are your variables measured accurately?
# 3. Reverse Causality: Does the DV also cause the IV?
# → These affect INTERNAL VALIDITY (causal interpretation).


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 8: OUTLIER DIAGNOSTICS                                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# Calculate four key outlier diagnostics
stud_resid <- rstudent(final_model)       # Studentized Residuals
leverage   <- hatvalues(final_model)      # Leverage (hat values)
cooksd     <- cooks.distance(final_model) # Cook's Distance
dffits_val <- dffits(final_model)         # DFFITS

# Store diagnostics in a data frame
outlier_df <- data.frame(
  obs        = 1:length(stud_resid),
  stud_resid = stud_resid,
  leverage   = leverage,
  cooksd     = cooksd,
  dffits     = dffits_val
)

# --- Define thresholds ---
k <- length(coef(final_model)) - 1   # Number of predictors (excluding intercept)
n <- nobs(final_model)               # Sample size

crit_resid   <- 2                         # |studentized residual| > 2
crit_leverage <- (2 * k + 2) / n          # leverage > (2k + 2) / n
crit_cooks   <- 4 / n                     # Cook's D > 4/n
crit_dffits  <- 2 * sqrt(k / n)           # |DFFITS| > 2 * sqrt(k/n)

# --- Flag outliers (any threshold exceeded) ---
outlier_df$is_outlier <- ifelse(
  abs(stud_resid) > crit_resid |
  leverage > crit_leverage |
  cooksd > crit_cooks |
  abs(dffits_val) > crit_dffits,
  1, 0
)

# How many outliers were flagged?
cat("Outliers flagged:", sum(outlier_df$is_outlier), "out of", n, "\n")

# View the flagged observations:
outlier_df %>% filter(is_outlier == 1)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 9: RE-RUN REGRESSIONS WITHOUT OUTLIERS (Robustness Check)       ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# Remove the flagged outliers from the dataset
data_nooutliers <- data_clean[outlier_df$is_outlier == 0, ]

# Re-run ALL models on the cleaned data
model1_clean <- lm(<DV> ~ <IV>, data = data_nooutliers)
model2_clean <- lm(<DV> ~ <IV> + <control_1>, data = data_nooutliers)
model3_clean <- lm(<DV> ~ <IV> + <control_1> + <control_2>, data = data_nooutliers)
model4_clean <- lm(<DV> ~ <IV> + <control_1> + <control_2> + <control_3>,
                   data = data_nooutliers)

# Robust SEs for the cleaned models
robust_se_clean <- list(
  sqrt(diag(vcovHC(model1_clean, type = "HC1"))),
  sqrt(diag(vcovHC(model2_clean, type = "HC1"))),
  sqrt(diag(vcovHC(model3_clean, type = "HC1"))),
  sqrt(diag(vcovHC(model4_clean, type = "HC1")))
)

robust_p_clean <- list(
  coeftest(model1_clean, vcov. = vcovHC(model1_clean, type = "HC1"))[, 4],
  coeftest(model2_clean, vcov. = vcovHC(model2_clean, type = "HC1"))[, 4],
  coeftest(model3_clean, vcov. = vcovHC(model3_clean, type = "HC1"))[, 4],
  coeftest(model4_clean, vcov. = vcovHC(model4_clean, type = "HC1"))[, 4]
)

# Stargazer table for outlier-excluded models
stargazer(
  model1_clean, model2_clean, model3_clean, model4_clean,
  type = "text",
  title = "Regression Results (Outliers Removed)",
  dep.var.labels = "<DV Label>",
  covariate.labels = c(
    "<IV Label>",
    "<Control 1 Label>",
    "<Control 2 Label>",
    "<Control 3 Label>"
  ),
  se = robust_se_clean,
  p  = robust_p_clean,
  omit.stat = c("f", "ser"),
  add.lines = list(
    c("Robust SEs", "HC1", "HC1", "HC1", "HC1")
  ),
  notes = "HC1 robust standard errors in parentheses. Outliers removed.",
  out = "regression_table_no_outliers.txt"
)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 10: INTERACTION TERMS (if the exam asks for one)                ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# --- 10a. Continuous x Categorical Interaction ---
# The * operator adds both main effects AND the interaction automatically
model_interact <- lm(<DV> ~ <continuous_IV> * <categorical_var> + <controls>,
                     data = data_clean)
summary(model_interact)

# Visualize the interaction with ggpredict
# terms = c("x-axis variable", "color/group variable")
pred <- ggpredict(model_interact, terms = c("<continuous_IV>", "<categorical_var>"))
plot(pred) +
  labs(
    title = "Interaction Effect",
    x = "<IV label>",
    y = "Predicted <DV>",
    color = "<Categorical Var>"
  ) +
  theme_minimal()

# --- 10b. Continuous x Continuous Interaction ---
model_cont_int <- lm(<DV> ~ <IV1> * <IV2> + <controls>, data = data_clean)
summary(model_cont_int)

# Visualize at representative values of the moderator
pred2 <- ggpredict(model_cont_int, terms = c("<IV1>", "<IV2> [-2, -1, 0, 1, 2]"))
plot(pred2) +
  labs(
    title = "Interaction: <IV1> x <IV2>",
    x = "<IV1>",
    y = "Predicted <DV>",
    color = "<IV2> level"
  ) +
  theme_minimal()

# --- 10c. Stargazer for interaction models ---
stargazer(model_interact, type = "text",
          title = "Interaction Model Results",
          out = "interaction_table.txt")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 11: FIXED EFFECTS (if the exam involves panel-like structure)   ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# Fixed effects = adding factor() dummies for a grouping variable.
# This controls for all time-invariant characteristics of each group.

# Justice fixed effects (example from HW3):
# model_fe <- lm(<DV> ~ <IV> + factor(<group_var>), data = data_clean)

# Justice + Year fixed effects:
# model_fe2 <- lm(<DV> ~ <IV> + factor(<group_var>) + factor(<year_var>), data = data_clean)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 12: QUICK INTERPRETATION CHEAT SHEET (Comments Only)          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# --- Reading Regression Output ---
# Coefficient (Estimate): A 1-unit increase in X is associated with a
#   [coefficient]-unit change in Y, holding all else constant.
#
# Standard Error: Measures uncertainty around the coefficient estimate.
#   Smaller SE = more precise estimate.
#
# p-value: Probability of seeing this result if the true effect were 0.
#   p < 0.05 → statistically significant at the 5% level.
#   p < 0.01 → significant at the 1% level.
#
# R-squared: Proportion of variance in Y explained by the model.
#   Higher = better fit, but adding variables always increases it.
#
# Adjusted R-squared: Penalizes for adding useless variables.
#   Use this to compare models with different numbers of predictors.

# --- Interpreting Log Transformations ---
# If DV is log(Y) and IV is X:
#   A 1-unit increase in X → approximately (coefficient * 100)% change in Y.
#   More precisely: % change = (exp(coefficient) - 1) * 100
#
# If DV is log(Y) and IV is log(X):
#   A 1% increase in X → coefficient% change in Y (elasticity).

# --- Interpreting Interaction Terms ---
# Y ~ X1 * X2 expands to: Y ~ X1 + X2 + X1:X2
# The coefficient on X1:X2 tells you how the effect of X1 on Y
#   CHANGES for each 1-unit increase in X2 (and vice versa).
# To get the total effect of X1 at a specific X2 value:
#   Total effect of X1 = beta_X1 + beta_X1:X2 * (value of X2)

# --- Interpreting Dummy/Binary Variables ---
# Coefficient on a dummy = difference in Y between the group coded 1
#   and the reference group (coded 0), holding all else constant.

# --- HC1 Robust Standard Errors ---
# Use when heteroskedasticity is detected (BP test p < 0.05).
# Robust SEs do NOT change coefficient estimates — only the SEs and p-values.
# Always safer to report robust SEs as your main results.

# --- OVB Direction ---
# When you ADD a control and the IV coefficient:
#   Moves TOWARD zero → the omitted variable was biasing it AWAY from zero
#     (upward bias if positive, downward bias if negative).
#   Moves AWAY from zero → the omitted variable was attenuating the effect.
#   Stays roughly the same → that control wasn't causing much bias.


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 13: SAVE PLOTS                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# Save the last plot you printed:
# ggsave("<filename>.png", width = 8, height = 6, dpi = 300)

# Save a specific plot object:
# ggsave("<filename>.png", plot = <plot_object>, width = 8, height = 6, dpi = 300)
