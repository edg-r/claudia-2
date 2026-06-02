# QM2 Final Exam Script
# Name: Edgar Agunias
# Date: 2026-03-17

# ---------------------------
# 1. Setup
# ---------------------------

# Clear the current R environment so old objects do not affect the exam script.
rm(list = ls())

# Set the folder where the exam files are stored and verify the path.
#setwd("/Users/edgar/Desktop/QM2 Final")
#getwd()

# Load only common course libraries used in the labs and homework files.
library(tidyverse)
library(readxl)
library(ggplot2)
library(stargazer)

# Simple HTML escaping so manual tables can be exported cleanly.
html_escape <- function(x) {
  x <- gsub("&", "&amp;", x, fixed = TRUE)
  x <- gsub("<", "&lt;", x, fixed = TRUE)
  x <- gsub(">", "&gt;", x, fixed = TRUE)
  x
}

# Write a data frame to a minimal HTML table without extra packages.
write_simple_html_table <- function(df, file, title = "Table") {
  header <- paste0("<th>", html_escape(names(df)), "</th>", collapse = "")
  rows <- apply(df, 1, function(row) {
    cells <- paste0("<td>", html_escape(as.character(row)), "</td>", collapse = "")
    paste0("<tr>", cells, "</tr>")
  })

  html <- c(
    "<!DOCTYPE html>",
    "<html>",
    "<head>",
    "  <meta charset=\"utf-8\">",
    paste0("  <title>", html_escape(title), "</title>"),
    "  <style>",
    "    body{font-family:Arial,sans-serif;margin:24px;}",
    "    table{border-collapse:collapse;width:100%;max-width:1100px;}",
    "    th,td{border:1px solid #ccc;padding:8px;text-align:left;}",
    "    th{background:#f3f3f3;}",
    "  </style>",
    "</head>",
    "<body>",
    paste0("  <h2>", html_escape(title), "</h2>"),
    "  <table>",
    paste0("    <tr>", header, "</tr>"),
    paste0("    ", rows),
    "  </table>",
    "</body>",
    "</html>"
  )

  writeLines(html, file)
}

# Build an HC1 robust variance-covariance matrix manually so the script
# does not depend on extra packages that may be missing on exam day.
hc1_vcov <- function(model) {
  X <- model.matrix(model)
  u <- residuals(model)
  n <- nrow(X)
  k <- ncol(X)
  bread <- solve(t(X) %*% X)
  meat <- t(X) %*% (X * (u^2))
  (n / (n - k)) * bread %*% meat %*% bread
}

# Convert the robust variance matrix into robust standard errors.
hc1_se <- function(model) {
  sqrt(diag(hc1_vcov(model)))
}

# Create a clean regression-output table with coefficient, robust SE, t-stat, and p-value.
robust_test_table <- function(model) {
  beta <- coef(model)
  se <- hc1_se(model)
  t_stat <- beta / se
  p_value <- 2 * pt(abs(t_stat), df = df.residual(model), lower.tail = FALSE)
  data.frame(
    term = names(beta),
    estimate = beta,
    robust_se = se,
    t_value = t_stat,
    p_value = p_value,
    row.names = NULL
  )
}

# Compute VIF values manually by regressing each predictor on the others.
# This checks whether the controls are too highly correlated with one another.
vif_manual <- function(model) {
  X <- model.matrix(model)[, -1, drop = FALSE]

  vif_values <- sapply(seq_len(ncol(X)), function(i) {
    y_i <- X[, i]
    x_i <- X[, -i, drop = FALSE]

    if (ncol(x_i) == 0) {
      return(1)
    }

    r_squared <- summary(lm(y_i ~ x_i))$r.squared
    1 / (1 - r_squared)
  })

  data.frame(
    variable = colnames(X),
    vif = vif_values,
    row.names = NULL
  )
}

# Run a simple Breusch-Pagan-style test for heteroskedasticity.
# If white = TRUE, include fitted values squared for a White-type version.
bp_test_manual <- function(model, white = FALSE) {
  resid_sq <- residuals(model)^2
  fitted_vals <- fitted(model)

  if (white) {
    aux_model <- lm(resid_sq ~ fitted_vals + I(fitted_vals^2))
    df_test <- 2
    test_name <- "White-type test"
  } else {
    aux_model <- lm(resid_sq ~ fitted_vals)
    df_test <- 1
    test_name <- "Breusch-Pagan-type test"
  }

  lm_stat <- nobs(model) * summary(aux_model)$r.squared
  p_value <- pchisq(lm_stat, df = df_test, lower.tail = FALSE)

  data.frame(
    test = test_name,
    statistic = lm_stat,
    df = df_test,
    p_value = p_value
  )
}

# Compare a linear model against a version with a squared X term.
# If the squared term is not statistically important, linearity looks more plausible.
linearity_check <- function(model, data, x_var, y_var, controls) {
  rhs_linear <- paste(c(x_var, controls), collapse = " + ")
  rhs_quad <- paste(c(x_var, paste0("I(", x_var, "^2)"), controls), collapse = " + ")

  linear_formula <- as.formula(paste(y_var, "~", rhs_linear))
  quad_formula <- as.formula(paste(y_var, "~", rhs_quad))

  linear_model <- lm(linear_formula, data = data)
  quad_model <- lm(quad_formula, data = data)
  quad_summary <- summary(quad_model)
  quad_term <- paste0("I(", x_var, "^2)")

  data.frame(
    test = "Quadratic-term check",
    statistic = quad_summary$coefficients[quad_term, "t value"],
    p_value = quad_summary$coefficients[quad_term, "Pr(>|t|)"],
    stringsAsFactors = FALSE
  )
}

# Create a compact table for residual normality diagnostics.
normality_check <- function(model) {
  shapiro_result <- shapiro.test(residuals(model))

  data.frame(
    test = "Shapiro-Wilk test",
    statistic = unname(shapiro_result$statistic),
    p_value = shapiro_result$p.value,
    stringsAsFactors = FALSE
  )
}

# ---------------------------
# 2. Load and clean data
# ---------------------------

# Read the simulation dataset from the exam workbook.
final_data <- read_excel("000 Exam/cross country dataset.xlsx", sheet = "simulation_data")

# Inspect the variable types and summary statistics before cleaning.
str(final_data)
summary(final_data)

# Keep all variables except the country name in a list for numeric conversion.
numeric_columns <- names(final_data)[names(final_data) != "entity"]

# Replace ".", "(D)", and similar placeholders with missing values,
# then convert the remaining analysis variables to numeric.
final_data <- final_data %>%
  mutate(across(all_of(numeric_columns), ~ ifelse(.x %in% c(".", "(D)"), NA, .x))) %>%
  mutate(across(all_of(numeric_columns), as.numeric))

# Main question:
# Does a larger increase in women's representation in parliament predict
# an improvement in the Gender Inequality Index (GII)?
# Lower GII means less gender inequality, so a negative change in GII is an improvement.

# Create the main independent and dependent variables.
# Also create percent-change versions for robustness and log GDP for easier interpretation.
analysis_data <- final_data %>%
  mutate(
    women_parliament_change =
      `share-of-women-in-parliament-2010s` - `share-of-women-in-parliament-1990s`,
    women_parliament_change_pct = ifelse(
      `share-of-women-in-parliament-1990s` != 0,
      100 * (women_parliament_change / `share-of-women-in-parliament-1990s`),
      NA
    ),
    gii_change =
      `gender-inequality-index-2010s` - `gender-inequality-index-1990s`,
    gii_change_pct = ifelse(
      `gender-inequality-index-1990s` != 0,
      100 * (gii_change / `gender-inequality-index-1990s`),
      NA
    ),
    log_gdp_pc = log(`gdp-per-capita-worldbank-2020`)
  ) %>%
  select(
    entity,
    `share-of-women-in-parliament-1990s`,
    `share-of-women-in-parliament-2010s`,
    women_parliament_change,
    women_parliament_change_pct,
    gii_change,
    gii_change_pct,
    `gender-inequality-index-1990s`,
    `gender-inequality-index-2010s`,
    log_gdp_pc,
    `democracy-index-eiu-2020`,
    `ti-corruption-perception-index-2018`,
    `liberal-democracy`,
    `maternal-mortality-2010s`
  ) %>%
  drop_na()

# Check the final analysis sample after all missing values are removed.
summary(analysis_data)

# Build a compact summary-statistics dataset for the main analysis variables.
summary_data <- analysis_data %>%
  select(
    `share-of-women-in-parliament-1990s`,
    `share-of-women-in-parliament-2010s`,
    women_parliament_change,
    women_parliament_change_pct,
    gii_change,
    gii_change_pct,
    `gender-inequality-index-1990s`,
    `gender-inequality-index-2010s`,
    log_gdp_pc,
    `democracy-index-eiu-2020`,
    `ti-corruption-perception-index-2018`,
    `liberal-democracy`,
    `maternal-mortality-2010s`
  )

# Create a manual summary-statistics table that is easy to inspect and export.
summary_table <- data.frame(
  variable = names(summary_data),
  n = sapply(summary_data, function(x) sum(!is.na(x))),
  mean = sapply(summary_data, function(x) mean(x, na.rm = TRUE)),
  sd = sapply(summary_data, function(x) sd(x, na.rm = TRUE)),
  min = sapply(summary_data, function(x) min(x, na.rm = TRUE)),
  max = sapply(summary_data, function(x) max(x, na.rm = TRUE)),
  row.names = NULL
)

print(summary_table)

summary_table_export <- summary_table
summary_table_export[, -1] <- round(summary_table_export[, -1], 3)

write_simple_html_table(
  summary_table_export,
  file = "summary_statistics_table.html",
  title = "Summary Statistics"
)

# ---------------------------
# 3. Descriptive plots
# ---------------------------

# Plot the main percent-change relationship used in the regression analysis.
plot_1 <- ggplot(
  analysis_data,
  aes(x = women_parliament_change_pct, y = gii_change_pct)
) +
  geom_point(color = "steelblue", alpha = 0.7, size = 2) +
  geom_smooth(method = "lm", se = TRUE, color = "darkred") +
  labs(
    title = "Percent Change in Women in Parliament and Percent Change in GII",
    x = "Percent change in women's share of parliament seats",
    y = "Percent change in Gender Inequality Index",
    caption = "Negative values on the y-axis indicate an improvement in GII."
  ) +
  theme_minimal()

print(plot_1)

# Save the main percent-change figure.
ggsave(
  filename = "gii_pct_vs_women_parliament_pct_main.png",
  plot = plot_1,
  width = 8,
  height = 6,
  dpi = 300
)

# Trim extreme percent-change values for a simple robustness plot.
analysis_trimmed <- analysis_data %>%
  filter(abs(women_parliament_change_pct) < 1000)

# Plot the trimmed percent-change version after dropping extreme outliers.
plot_2 <- ggplot(
  analysis_trimmed,
  aes(x = women_parliament_change_pct, y = gii_change_pct)
) +
  geom_point(color = "steelblue", alpha = 0.7, size = 2) +
  geom_smooth(method = "lm", se = TRUE, color = "darkred") +
  labs(
    title = "Percent Change in Women in Parliament and Percent Change in GII",
    x = "Percent change in women's share of parliament seats",
    y = "Percent change in Gender Inequality Index",
    caption = "This version trims extreme percent-change values."
  ) +
  theme_minimal()

print(plot_2)

# Save the trimmed percent-change figure.
ggsave(
  filename = "gii_pct_vs_women_parliament_pct.png",
  plot = plot_2,
  width = 8,
  height = 6,
  dpi = 300
)

# ---------------------------
# 4. Regression models
# ---------------------------

# Model 1 is the main bivariate percent-change regression:
# does a percent increase in women's parliament share predict a percent change in GII?
model_1 <- lm(gii_change_pct ~ women_parliament_change_pct, data = analysis_trimmed)

# Model 2 adds economic development as a control.
model_2 <- lm(
  gii_change_pct ~ women_parliament_change_pct + log_gdp_pc,
  data = analysis_trimmed
)

# Model 3 adds the democracy index to account for regime differences.
model_3 <- lm(
  gii_change_pct ~ women_parliament_change_pct + log_gdp_pc +
    `democracy-index-eiu-2020`,
  data = analysis_trimmed
)

# Model 4 adds corruption perceptions as a final governance control.
model_4 <- lm(
  gii_change_pct ~ women_parliament_change_pct + log_gdp_pc +
    `democracy-index-eiu-2020` +
    `ti-corruption-perception-index-2018`,
  data = analysis_trimmed
)

# Alternative specification controlling for baseline GII directly.
# This version keeps the percent-change X but predicts the 2010s GII level while holding baseline GII fixed.
model_5 <- lm(
  `gender-inequality-index-2010s` ~ women_parliament_change_pct +
    `gender-inequality-index-1990s` + log_gdp_pc +
    `democracy-index-eiu-2020` +
    `ti-corruption-perception-index-2018`,
  data = analysis_trimmed
)

# Collect HC1 robust standard errors for the four main models.
robust_se_main <- list(
  hc1_se(model_1),
  hc1_se(model_2),
  hc1_se(model_3),
  hc1_se(model_4)
)

# Export the main regression table with robust standard errors.
stargazer(
  model_1, model_2, model_3, model_4,
  type = "html",
  title = "Regression Results: Percent Change in GII and Percent Change in Women in Parliament",
  dep.var.labels = "Percent Change in Gender Inequality Index",
  covariate.labels = c(
    "Percent change in women's parliament share",
    "Log GDP per capita",
    "Democracy Index",
    "Corruption Perceptions Index"
  ),
  se = robust_se_main,
  omit.stat = c("f", "ser"),
  add.lines = list(
    c("Robust SEs", "HC1", "HC1", "HC1", "HC1")
  ),
  notes = "HC1 robust standard errors in parentheses.",
  out = "final_regression_table.html"
)

# Export the alternative baseline-controlled specification separately.
stargazer(
  model_5,
  type = "html",
  title = "Alternative Model: 2010s GII with Baseline GII Control",
  dep.var.labels = "Gender Inequality Index (2010s)",
  covariate.labels = c(
    "Percent change in women's parliament share",
    "Gender Inequality Index (1990s)",
    "Log GDP per capita",
    "Democracy Index",
    "Corruption Perceptions Index"
  ),
  se = list(hc1_se(model_5)),
  notes = "HC1 robust standard errors in parentheses.",
  out = "final_regression_table_alt.html"
)

# Print regular OLS summaries and then the HC1 robust inference table for the two main results.
summary(model_4)
robust_test_table(model_4)
summary(model_5)
robust_test_table(model_5)

# ---------------------------
# 5. Diagnostics
# ---------------------------

# Store residuals and fitted values from the preferred percent-change model for diagnostic plotting.
analysis_trimmed$residuals <- residuals(model_4)
analysis_trimmed$fittedvals <- fitted(model_4)

# Residual-vs-fitted plot:
# look for random scatter around zero rather than a curve or funnel shape.
ggplot(analysis_trimmed, aes(x = fittedvals, y = residuals)) +
  geom_point(color = "steelblue") +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
  labs(
    title = "Residuals vs Fitted Values",
    x = "Fitted values",
    y = "Residuals"
  ) +
  theme_minimal()

# 1. Linear in parameters:
# add a squared X term as a quick check for obvious nonlinearity.
linearity_results <- linearity_check(
  model = model_4,
  data = analysis_trimmed,
  x_var = "women_parliament_change_pct",
  y_var = "gii_change_pct",
  controls = c(
    "log_gdp_pc",
    "`democracy-index-eiu-2020`",
    "`ti-corruption-perception-index-2018`"
  )
)

# 2. No multicollinearity:
# VIF values well below 10 are usually treated as acceptable.
vif_results <- vif_manual(model_4)

# 5. Heteroskedasticity:
# use BP and White-style tests, then report HC1 robust standard errors in the regressions.
bp_results <- bp_test_manual(model_4)
white_results <- bp_test_manual(model_4, white = TRUE)

# 6. Bonus normality check:
# normality is not required for Gauss-Markov unbiasedness, but it is a common extra check.
normality_results <- normality_check(model_4)

# Combine the testable assumptions into one exportable diagnostics table.
diagnostics_table <- bind_rows(
  linearity_results,
  bp_results,
  white_results,
  normality_results
) %>%
  mutate(
    statistic = round(statistic, 3),
    p_value = round(p_value, 4)
  )

print(vif_results)
print(diagnostics_table)

vif_results_export <- vif_results
vif_results_export$vif <- round(vif_results_export$vif, 3)

write_simple_html_table(
  vif_results_export,
  file = "gauss_markov_vif_table.html",
  title = "Gauss-Markov Diagnostics: Multicollinearity (VIF)"
)

write_simple_html_table(
  diagnostics_table,
  file = "gauss_markov_test_table.html",
  title = "Gauss-Markov Diagnostics: Formal Tests"
)

# Build a short assumption checklist for the assumptions that are partly qualitative.
assumption_checklist <- data.frame(
  assumption = c(
    "1. Linear in parameters",
    "2. No multicollinearity",
    "3. Random sampling",
    "4. Exogeneity / Zero conditional mean",
    "5. Heteroskedasticity",
    "6. Bonus: Normal distribution"
  ),
  how_checked = c(
    "Residual-vs-fitted plot and quadratic term check",
    "Variance inflation factors (VIF)",
    "Qualitative caveat: cross-country observational sample, not guaranteed random",
    "Qualitative caveat: omitted variables and reverse causality may remain",
    "Breusch-Pagan-type and White-type tests; HC1 robust SE applied",
    "Shapiro-Wilk test on residuals"
  ),
  takeaway = c(
    "If the squared term is insignificant and the residual plot is roughly patternless, linearity is more plausible",
    "Low VIF values suggest multicollinearity is not severe",
    "Cannot be fully verified with the dataset; discuss as a limitation",
    "Cannot be proven with the data; discuss controls plus remaining endogeneity risk",
    "If variance is not constant, robust SEs address inference",
    "Useful descriptive check, but not required for Gauss-Markov"
  ),
  stringsAsFactors = FALSE
)

write_simple_html_table(
  assumption_checklist,
  file = "gauss_markov_assumption_checklist.html",
  title = "Gauss-Markov Assumption Checklist"
)

# Qualitative discussion still matters for:
# 1. omitted variable bias
# 2. reverse causality
# 3. sample representativeness

# ---------------------------
# 6. Interaction analysis: liberal vs non-liberal democracies
# ---------------------------

# Estimate whether the effect of changes in women's parliamentary representation
# differs between liberal democracies and non-liberal democracies.
model_interaction <- lm(
  gii_change_pct ~ women_parliament_change_pct * `liberal-democracy` +
    log_gdp_pc +
    `democracy-index-eiu-2020` +
    `ti-corruption-perception-index-2018`,
  data = analysis_trimmed
)

# Export the interaction regression table to a separate folder.
stargazer(
  model_interaction,
  type = "html",
  title = "Interaction Model: Percent Change in GII by Liberal Democracy Status",
  dep.var.labels = "Percent Change in Gender Inequality Index",
  covariate.labels = c(
    "Percent change in women's parliament share",
    "Liberal democracy",
    "Women parliament change x liberal democracy",
    "Log GDP per capita",
    "Democracy Index",
    "Corruption Perceptions Index"
  ),
  se = list(hc1_se(model_interaction)),
  notes = "HC1 robust standard errors in parentheses.",
  out = "interaction_analysis/interaction_regression_table.html"
)

# Store robust results for the interaction model in a separate HTML table.
interaction_robust <- robust_test_table(model_interaction)
interaction_robust_export <- interaction_robust
interaction_robust_export[, -1] <- round(interaction_robust_export[, -1], 4)

write_simple_html_table(
  interaction_robust_export,
  file = "interaction_analysis/interaction_robust_results.html",
  title = "Interaction Model Robust Results"
)

# Create fitted values for liberal and non-liberal democracies across the observed X range.
x_grid <- seq(
  min(analysis_trimmed$women_parliament_change_pct, na.rm = TRUE),
  max(analysis_trimmed$women_parliament_change_pct, na.rm = TRUE),
  length.out = 100
)

interaction_plot_data <- expand.grid(
  women_parliament_change_pct = x_grid,
  `liberal-democracy` = c(0, 1)
)

interaction_plot_data$log_gdp_pc <- mean(analysis_trimmed$log_gdp_pc, na.rm = TRUE)
interaction_plot_data$`democracy-index-eiu-2020` <- mean(analysis_trimmed$`democracy-index-eiu-2020`, na.rm = TRUE)
interaction_plot_data$`ti-corruption-perception-index-2018` <- mean(analysis_trimmed$`ti-corruption-perception-index-2018`, na.rm = TRUE)
interaction_plot_data$predicted_gii_change_pct <- predict(model_interaction, newdata = interaction_plot_data)
interaction_plot_data$regime_type <- ifelse(
  interaction_plot_data$`liberal-democracy` == 1,
  "Liberal democracy",
  "Non-liberal democracy"
)

# Plot separate fitted lines for liberal and non-liberal democracies.
interaction_plot <- ggplot() +
  geom_point(
    data = analysis_trimmed,
    aes(
      x = women_parliament_change_pct,
      y = gii_change_pct,
      color = factor(`liberal-democracy`)
    ),
    alpha = 0.55,
    size = 2
  ) +
  geom_line(
    data = interaction_plot_data,
    aes(
      x = women_parliament_change_pct,
      y = predicted_gii_change_pct,
      color = regime_type
    ),
    linewidth = 1.1
  ) +
  scale_color_manual(
    values = c(
      "0" = "gray40",
      "1" = "steelblue",
      "Non-liberal democracy" = "gray40",
      "Liberal democracy" = "steelblue"
    ),
    labels = c(
      "0" = "Non-liberal democracy",
      "1" = "Liberal democracy",
      "Non-liberal democracy" = "Non-liberal democracy",
      "Liberal democracy" = "Liberal democracy"
    )
  ) +
  labs(
    title = "Interaction Effect of Women's Parliament Share by Regime Type",
    x = "Percent change in women's share of parliament seats",
    y = "Predicted percent change in GII",
    color = "Regime type",
    caption = "Lines show fitted values from the interaction model, holding controls at their sample means."
  ) +
  theme_minimal()

print(interaction_plot)

ggsave(
  filename = "interaction_analysis/interaction_effect_plot.png",
  plot = interaction_plot,
  width = 8,
  height = 6,
  dpi = 300
)

# ---------------------------
# 7. Outlier check and robustness
# ---------------------------

# Create common influence statistics to flag observations that may drive results too strongly.
stud_resid <- rstudent(model_4)
leverage <- hatvalues(model_4)
cooksd <- cooks.distance(model_4)
dffits_values <- dffits(model_4)

# Put the influence diagnostics into one data frame so flagged countries can be reviewed.
outlier_df <- data.frame(
  entity = analysis_trimmed$entity,
  abs_stud_resid = abs(stud_resid),
  leverage = leverage,
  abs_dffits = abs(dffits_values),
  cooksd = cooksd
)

# Define conventional cutoffs for leverage, Cook's distance, and DFFITS.
k <- length(coef(model_4))
n <- nobs(model_4)
crit_leverage <- (2 * k + 2) / n
crit_cooks <- 4 / n
crit_dffits <- 2 * sqrt(k / n)

# Mark any observation as an outlier if it crosses at least one threshold.
outlier_df$outlier <- ifelse(
  abs(stud_resid) > 2 |
    leverage > crit_leverage |
    cooksd > crit_cooks |
    abs(dffits_values) > crit_dffits,
  1,
  0
)

# Create a reduced sample without flagged outliers.
analysis_no_outliers <- analysis_trimmed[outlier_df$outlier == 0, ]

# Re-estimate the preferred percent-change model on the no-outlier sample.
model_4_no_outliers <- lm(
  gii_change_pct ~ women_parliament_change_pct + log_gdp_pc +
    `democracy-index-eiu-2020` +
    `ti-corruption-perception-index-2018`,
  data = analysis_no_outliers
)

# Compare the preferred model in the full sample against the no-outlier sample.
stargazer(
  model_4, model_4_no_outliers,
  type = "html",
  title = "Robustness Check: Percent-Change Model, Full Sample vs No Outliers",
  dep.var.labels = "Percent Change in Gender Inequality Index",
  column.labels = c("Full sample", "No outliers"),
  covariate.labels = c(
    "Percent change in women's parliament share",
    "Log GDP per capita",
    "Democracy Index",
    "Corruption Perceptions Index"
  ),
  se = list(
    hc1_se(model_4),
    hc1_se(model_4_no_outliers)
  ),
  notes = "HC1 robust standard errors in parentheses.",
  out = "final_regression_outlier_check.html"
)

# Print robust results for the no-outlier model.
robust_test_table(model_4_no_outliers)

# ---------------------------
# 8. Optional percent-change robustness model
# ---------------------------

# Estimate the same percent-change model again as a clearly labeled fallback object.
model_pct <- lm(
  gii_change_pct ~ women_parliament_change_pct + log_gdp_pc +
    `democracy-index-eiu-2020` +
    `ti-corruption-perception-index-2018`,
  data = analysis_trimmed
)

# Print both the standard OLS summary and the HC1 robust inference table.
summary(model_pct)
robust_test_table(model_pct)
