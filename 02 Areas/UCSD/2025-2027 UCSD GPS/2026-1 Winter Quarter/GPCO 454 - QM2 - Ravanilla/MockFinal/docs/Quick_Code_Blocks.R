# Quick Code Blocks for the Mock Final
# Single-file exam backup.
# Change the placeholder names only.
# This file combines the code blocks and the notes you are most likely to need.

# ---------------------------
# 0. Working directory
# ---------------------------

# Use setwd() first so R can find your files.
# Replace the path with the folder where your exam files are stored.
# Then run getwd() to confirm.

setwd("/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/MockFinal")
getwd()

# If you are working from a different folder on exam day, replace the path above.
# After setwd(), all read/write commands look in that folder by default.

# ---------------------------
# 1. Packages and data
# ---------------------------

library(tidyverse)
library(readxl)
library(ggplot2)
library(stargazer)
library(modelsummary)
library(lmtest)
library(sandwich)
library(car)
library(ggeffects)

# First thing to do after loading packages:
# 1. Read the file
# 2. Inspect structure
# 3. Check summary statistics

data <- read_excel("YOUR_FILE.xlsx")
str(data)
summary(data)

# ---------------------------
# 2. Clean values
# ---------------------------

# If variables were imported as text, convert them.
# This is especially common when the sheet contains "." or "(D)".

cols_to_fix <- c("VAR1", "VAR2", "VAR3")

data <- data %>%
  mutate(across(all_of(cols_to_fix), ~ ifelse(.x %in% c(".", "(D)"), NA, .x))) %>%
  mutate(across(all_of(cols_to_fix), as.numeric))

# If only one variable needs conversion:
# data <- data %>% mutate(YOUR_VAR = as.numeric(YOUR_VAR))

# If you want to drop rows with missing values in the final analysis sample:
# data <- data %>% na.omit()

# ---------------------------
# 3. Merge behavior
# ---------------------------

# Important rule: before merging, make sure the key column has the same type in both datasets.
# If one ID is numeric and the other is character, the merge may fail or behave badly.

df1 <- df1 %>% mutate(ID = as.character(ID))
df2 <- df2 %>% mutate(ID = as.character(ID))

# Base R merge behavior:
# merge(df1, df2, by = "ID") is basically an inner join.
# It keeps only rows that match in both datasets.

inner_data <- merge(df1, df2, by = "ID")
left_data <- merge(df1, df2, by = "ID", all.x = TRUE)   # keep all rows from df1
right_data <- merge(df1, df2, by = "ID", all.y = TRUE)  # keep all rows from df2
full_data <- merge(df1, df2, by = "ID", all = TRUE)     # keep all rows from both

# Tidyverse versions
joined_data <- left_join(df1, df2, by = "ID")
inner_joined_data <- inner_join(df1, df2, by = "ID")
full_joined_data <- full_join(df1, df2, by = "ID")

# ---------------------------
# 4. Filter using a list
# ---------------------------

# Use %in% when you want to keep only rows from a specific list.

keep_list <- c("A", "B", "C")

filtered_data <- data %>%
  filter(GROUP_VAR %in% keep_list)

# To drop rows from a specific list:
# data <- data %>% filter(!GROUP_VAR %in% keep_list)

# ---------------------------
# 5. Create variables
# ---------------------------

# Typical exam transformations:
# 1. Difference
# 2. Percent change
# 3. Dummy variable
# 4. Categorical variable with case_when()

data <- data %>%
  mutate(
    NEW_VAR = OLD_VAR1 - OLD_VAR2,
    PERCENT_CHANGE = ifelse(OLD_VAR2 != 0, 100 * ((OLD_VAR1 - OLD_VAR2) / OLD_VAR2), NA),
    DUMMY_VAR = ifelse(X_VAR > median(X_VAR, na.rm = TRUE), 1, 0),
    CATEGORY_VAR = case_when(
      YEAR_VAR < 2000 ~ "Before 2000",
      YEAR_VAR >= 2000 & YEAR_VAR < 2010 ~ "2000s",
      YEAR_VAR >= 2010 ~ "2010s"
    )
  )

data$CATEGORY_VAR <- factor(data$CATEGORY_VAR, levels = c("Before 2000", "2000s", "2010s"))

# If your prompt asks about effects over time or by group, creating a factor is often useful.

# ---------------------------
# 6. Regression sequence
# ---------------------------

# Safe regression workflow:
# 1. Start bivariate
# 2. Add controls one at a time
# 3. Report robust HC1 standard errors
# 4. Check diagnostics

model_1 <- lm(Y_VAR ~ X_VAR, data = data)
model_2 <- lm(Y_VAR ~ X_VAR + CONTROL_1, data = data)
model_3 <- lm(Y_VAR ~ X_VAR + CONTROL_1 + CONTROL_2, data = data)
model_4 <- lm(Y_VAR ~ X_VAR + CONTROL_1 + CONTROL_2 + CONTROL_3, data = data)

summary(model_4)

# ---------------------------
# 6A. Robust standard errors
# ---------------------------

# The mock final uses HC1 robust standard errors.
# Use vcovHC() from sandwich and coeftest() from lmtest.
# If heteroskedasticity is present, robust SEs fix the standard errors, not the coefficient itself.

robust_se <- list(
  sqrt(diag(vcovHC(model_1, type = "HC1"))),
  sqrt(diag(vcovHC(model_2, type = "HC1"))),
  sqrt(diag(vcovHC(model_3, type = "HC1"))),
  sqrt(diag(vcovHC(model_4, type = "HC1")))
)

stargazer(
  model_1, model_2, model_3, model_4,
  type = "text",
  title = "Regression Results",
  dep.var.labels = "Dependent variable",
  se = robust_se,
  out = "regression_table.txt"
)

# Fastest way to see robust inference for one model:
coeftest(model_4, vcov = vcovHC(model_4, type = "HC1"))

# If you want robust p-values for several models:
robust_p <- list(
  coeftest(model_1, vcov. = vcovHC(model_1, type = "HC1"))[, 4],
  coeftest(model_2, vcov. = vcovHC(model_2, type = "HC1"))[, 4],
  coeftest(model_3, vcov. = vcovHC(model_3, type = "HC1"))[, 4],
  coeftest(model_4, vcov. = vcovHC(model_4, type = "HC1"))[, 4]
)

# Interpretation note:
# "Because heteroskedasticity is a concern, I report HC1 robust standard errors."

# ---------------------------
# 7. Fixed effects and interaction
# ---------------------------

# Fixed effects are useful when you want to control for stable differences across people, places, or years.
# factor(PERSON_ID) = person fixed effects
# factor(YEAR_VAR) = year fixed effects

model_fe <- lm(Y_VAR ~ X_VAR + CONTROL_1 + factor(PERSON_ID), data = data)
model_year_fe <- lm(Y_VAR ~ X_VAR + CONTROL_1 + factor(YEAR_VAR), data = data)
model_int <- lm(Y_VAR ~ X_VAR * GROUP_VAR + CONTROL_1, data = data)

# Interaction interpretation:
# X_VAR coefficient = effect of X_VAR in the reference group.
# X_VAR:GROUP_VAR coefficient = how much the slope changes for another group.

# ---------------------------
# 8. Gauss-Markov checks
# ---------------------------

# Not all assumptions are tested the same way.
# Some are formal tests and some are qualitative judgments.

data$residuals <- residuals(model_4)
data$fittedvals <- fitted(model_4)

ggplot(data, aes(x = fittedvals, y = residuals)) +
  geom_point() +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red")

# What you want to see:
# random scatter around zero
# no obvious curve
# roughly constant spread

# If you see curvature, consider adding a squared term or changing the model specification.

vif(model_4)

# VIF guide:
# about 1 = no issue
# 1 to 5 = moderate but often acceptable
# above 10 = serious multicollinearity concern

bptest(model_4)
bptest(model_4, ~ fitted(model_4) + I(fitted(model_4)^2))

# Breusch-Pagan / White-type interpretation:
# p < 0.05 suggests heteroskedasticity
# If heteroskedasticity appears, keep using robust standard errors.

# Quadratic fix if needed
model_poly <- lm(Y_VAR ~ X_VAR + I(X_VAR^2) + CONTROL_1, data = data)

# Qualitative notes you can write in the exam:
# Random sampling issue -> threatens external validity.
# Endogeneity issue -> possible omitted variable bias, reverse causality, or measurement error.
# If endogeneity is present, the coefficient may not be causal.

# ---------------------------
# 9. Outlier / influence check
# ---------------------------

# Use these diagnostics for robustness.

stud_resid <- rstudent(model_4)
leverage <- hatvalues(model_4)
cooksd <- cooks.distance(model_4)
dffits_vals <- dffits(model_4)

k <- length(coef(model_4))
n <- nobs(model_4)

crit_leverage <- (2 * k + 2) / n
crit_cooks <- 4 / n
crit_dffit <- 2 * sqrt(k / n)

outlier_df <- data.frame(
  obs = 1:length(stud_resid),
  abs_stud_resid = abs(stud_resid),
  leverage = leverage,
  cooksd = cooksd,
  abs_dffits = abs(dffits_vals)
)

outlier_df$outlier <- ifelse(
  abs(stud_resid) > 2 |
    leverage > crit_leverage |
    cooksd > crit_cooks |
    abs(dffits_vals) > crit_dffit,
  1, 0
)

data_nooutliers <- data[outlier_df$outlier == 0, ]

model_4_nooutliers <- lm(Y_VAR ~ X_VAR + CONTROL_1 + CONTROL_2 + CONTROL_3, data = data_nooutliers)
coeftest(model_4_nooutliers, vcov = vcovHC(model_4_nooutliers, type = "HC1"))

# If results are similar after removing outliers, that strengthens the robustness claim.

# ---------------------------
# 10. Loops with named lists
# ---------------------------

# Use this pattern when you want to run the same model for many groups in a list.

group_codes <- list(
  GroupA = "A",
  GroupB = "B",
  GroupC = "C"
)

all_models <- list()
model_labels <- c()

for (group_name in names(group_codes)) {
  current_code <- group_codes[[group_name]]

  model_data <- data %>%
    filter(GROUP_VAR == current_code)

  current_model <- lm(Y_VAR ~ X_VAR + CONTROL_1, data = model_data)

  all_models <- append(all_models, list(current_model))
  model_labels <- append(model_labels, group_name)
}

# Alternative loop: summarize several variables by name
for (var_name in c("var1", "var2", "var3")) {
  print(summary(data[[var_name]]))
}

# ---------------------------
# 11. ggplot templates
# ---------------------------

# Scatterplot
ggplot(data, aes(x = X_VAR, y = Y_VAR)) +
  geom_point(alpha = 0.7) +
  theme_minimal() +
  labs(title = "Scatterplot Title", x = "X-axis label", y = "Y-axis label")

# Scatterplot with regression line
ggplot(data, aes(x = X_VAR, y = Y_VAR)) +
  geom_point(alpha = 0.7) +
  geom_smooth(method = "lm", se = TRUE, color = "blue") +
  theme_minimal() +
  labs(title = "Regression Plot", x = "X-axis label", y = "Y-axis label")

# Histogram
ggplot(data, aes(x = X_VAR)) +
  geom_histogram(binwidth = 1, fill = "skyblue", color = "black") +
  theme_minimal() +
  labs(title = "Histogram Title", x = "Variable", y = "Count")

# Boxplot by group
ggplot(data, aes(x = factor(GROUP_VAR), y = Y_VAR, fill = factor(GROUP_VAR))) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Boxplot Title", x = "Group", y = "Outcome")

# Line plot over time
ggplot(data, aes(x = YEAR_VAR, y = Y_VAR, color = GROUP_VAR)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  theme_minimal() +
  labs(title = "Trend Plot", x = "Year", y = "Outcome", color = "Group")

# Interaction plot from ggpredict()
pred_df <- ggpredict(model_int, terms = c("X_VAR", "GROUP_VAR"))

ggplot(pred_df, aes(x = x, y = predicted, color = group)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  geom_ribbon(aes(ymin = conf.low, ymax = conf.high, fill = group), alpha = 0.15, color = NA) +
  theme_minimal() +
  labs(title = "Predicted Values from Interaction Model", x = "X variable", y = "Predicted outcome")

# ---------------------------
# 12. Safe exam order
# ---------------------------

# 1. setwd()
# 2. load packages
# 3. read data
# 4. run str() and summary()
# 5. clean types and missing values
# 6. merge only after key types match
# 7. create variables with mutate()
# 8. make one basic plot
# 9. run bivariate model
# 10. add controls one at a time
# 11. report HC1 robust standard errors
# 12. check residual plot, vif(), and bptest()
# 13. if needed, rerun without outliers
# 14. if the prompt asks whether effects differ by group or time, run an interaction

# ---------------------------
# 13. Fast interpretation lines
# ---------------------------

# "The coefficient on X_VAR is positive/negative, meaning that as X_VAR increases, Y_VAR tends to increase/decrease."
# "This association is statistically significant at conventional levels."
# "After adding controls, the magnitude becomes larger/smaller, suggesting possible confounding."
# "Because heteroskedasticity is a concern, I report HC1 robust standard errors."
# "The residual plot does/does not suggest major nonlinearity."
# "The VIF values do/do not suggest serious multicollinearity."
# "This result should be interpreted cautiously because endogeneity and non-random sampling cannot be ruled out."
