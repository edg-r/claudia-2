# Mock Final Fallback Guide

This guide is a no-AI backup for the mock final. It is built from the patterns in:

- `/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/MockFinal/Mock Final.R`
- `/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/MockFinal/Week2_Lab.R`
- `/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/MockFinal/Week5_Lab.R`
- `/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/MockFinal/Week6_Lab.R`
- `/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/MockFinal/Week8_Lab_live.R`
- `/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/MockFinal/Agunias_A69046387_HW2.R`

Use this in order during the exam.

## 1. Basic setup

```r
library(tidyverse)
library(readxl)
library(ggplot2)
library(stargazer)
library(modelsummary)
library(lmtest)
library(sandwich)
library(car)
library(ggeffects)
```

Load data:

```r
data <- read_excel("YOUR_FILE.xlsx")
str(data)
summary(data)
```

If a variable should be numeric but imported as text:

```r
data <- data %>%
  mutate(YOUR_VAR = as.numeric(YOUR_VAR))
```

If missing values are stored as `"."` or `"(D)"`:

```r
cols_to_fix <- c("VAR1", "VAR2", "VAR3")

data <- data %>%
  mutate(across(all_of(cols_to_fix), ~ ifelse(.x %in% c(".", "(D)"), NA, .x))) %>%
  mutate(across(all_of(cols_to_fix), as.numeric))
```

## 2. Merge behavior

### Base R merge

Use this when your professor or prior scripts use `merge()`.

```r
merged_data <- merge(df1, df2, by = "ID")
```

Meaning:

- `by = "ID"` merges on the shared key column.
- Default behavior is like an inner join: keep only rows that match in both datasets.

Most common variants:

```r
# Inner join: keep only matching rows
merge(df1, df2, by = "ID", all.x = FALSE, all.y = FALSE)

# Left join: keep all rows from df1
merge(df1, df2, by = "ID", all.x = TRUE, all.y = FALSE)

# Right join: keep all rows from df2
merge(df1, df2, by = "ID", all.x = FALSE, all.y = TRUE)

# Full join: keep all rows from both
merge(df1, df2, by = "ID", all = TRUE)
```

### Tidyverse join

Use this when you want clearer syntax.

```r
left_join(df1, df2, by = "ID")
inner_join(df1, df2, by = "ID")
full_join(df1, df2, by = "ID")
```

### Important merge rule

Before merging, make sure the key has the same type in both datasets.

```r
df1 <- df1 %>% mutate(ID = as.character(ID))
df2 <- df2 %>% mutate(ID = as.character(ID))
```

## 3. Filtering with a specific list

Keep only rows that match a list:

```r
keep_list <- c("11", "31-33", "54,55,56", "92")

filtered_data <- data %>%
  filter(IndustryClassification %in% keep_list)
```

Drop rows that match a list:

```r
drop_list <- c("A", "B", "C")

filtered_data <- data %>%
  filter(!GROUP_VAR %in% drop_list)
```

## 4. Loop templates

### Loop through a named list of outcomes

This is the closest match to Week 5.

```r
outcome_variables <- list(
  Agriculture = "11",
  Manufacturing = "31-33",
  ProfServices = "54,55,56",
  Government = "92"
)

all_models <- list()
model_labels <- c()

for (outcome_name in names(outcome_variables)) {
  code_value <- outcome_variables[[outcome_name]]

  model_data <- data %>%
    filter(IndustryClassification == code_value)

  model_1 <- lm(Y_VAR ~ X_VAR, data = model_data)
  model_2 <- lm(Y_VAR ~ X_VAR + CONTROL_1 + CONTROL_2, data = model_data)

  all_models <- append(all_models, list(model_1, model_2))
  model_labels <- append(model_labels, c(outcome_name, outcome_name))
}
```

### Loop through rows of a lookup table

This is the closest match to HW2.

```r
specs <- tibble(
  group_code = c("11", "72"),
  table_title = c("Industry 11", "Industry 72")
)

results <- list()

for (i in seq_len(nrow(specs))) {
  current_code <- specs$group_code[[i]]
  current_title <- specs$table_title[[i]]

  reg_data <- data %>%
    filter(IndustryClassification == current_code)

  current_model <- lm(Y_VAR ~ X_VAR + CONTROL_1 + CONTROL_2, data = reg_data)

  results[[current_code]] <- list(
    title = current_title,
    model = current_model
  )
}
```

### Loop through variable names

Use this when you need the same operation for many columns.

```r
for (var_name in c("var1", "var2", "var3")) {
  print(summary(data[[var_name]]))
}
```

## 5. Regression sequence to use on the exam

This is the safest default structure.

### Step 1: Start with a simple model

```r
model_1 <- lm(Y_VAR ~ X_VAR, data = data_clean)
summary(model_1)
```

### Step 2: Add controls gradually

```r
model_2 <- lm(Y_VAR ~ X_VAR + CONTROL_1, data = data_clean)
model_3 <- lm(Y_VAR ~ X_VAR + CONTROL_1 + CONTROL_2, data = data_clean)
model_4 <- lm(Y_VAR ~ X_VAR + CONTROL_1 + CONTROL_2 + CONTROL_3, data = data_clean)
```

### Step 3: Report robust standard errors

Use HC1. That is exactly what the mock final uses.

```r
robust_se <- list(
  sqrt(diag(vcovHC(model_1, type = "HC1"))),
  sqrt(diag(vcovHC(model_2, type = "HC1"))),
  sqrt(diag(vcovHC(model_3, type = "HC1"))),
  sqrt(diag(vcovHC(model_4, type = "HC1")))
)

stargazer(
  model_1, model_2, model_3, model_4,
  type = "text",
  se = robust_se,
  out = "regression_table.txt"
)
```

If you want robust p-values too:

```r
coeftest(model_4, vcov = vcovHC(model_4, type = "HC1"))
```

### Step 4: Fixed effects if needed

Justice or person fixed effects:

```r
model_fe <- lm(Y_VAR ~ X_VAR + CONTROL_1 + factor(PERSON_ID), data = data_clean)
```

Year fixed effects:

```r
model_fe2 <- lm(Y_VAR ~ X_VAR + CONTROL_1 + factor(YEAR_VAR), data = data_clean)
```

### Step 5: Interaction if the question asks "does the effect differ by group?"

```r
model_int <- lm(Y_VAR ~ X_VAR * GROUP_VAR + CONTROL_1, data = data_clean)
summary(model_int)
```

Interpretation rule:

- Main `X_VAR` coefficient = effect when `GROUP_VAR` is at the reference category.
- Interaction term = how much the slope changes for another group.

## 6. Gauss-Markov and robustness checks

Not every assumption is tested the same way. Some are qualitative, some are formal tests.

### Linearity / model specification

Residuals should look randomly scattered around zero.

```r
data_clean$residuals <- residuals(model_4)
data_clean$fittedvals <- fitted(model_4)

ggplot(data_clean, aes(x = fittedvals, y = residuals)) +
  geom_point() +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red")
```

If you see a curve or strong pattern, consider:

- adding a missing control
- adding a squared term
- changing the functional form

Quadratic fix:

```r
model_poly <- lm(Y_VAR ~ X_VAR + I(X_VAR^2) + CONTROL_1, data = data_clean)
```

### Heteroskedasticity

Formal tests:

```r
bptest(model_4)
bptest(model_4, ~ fitted(model_4) + I(fitted(model_4)^2))
```

Interpretation:

- `p < 0.05`: evidence of heteroskedasticity
- solution: keep using robust standard errors

### Multicollinearity

```r
vif(model_4)
```

Quick interpretation:

- around `1`: no issue
- `1` to `5`: usually manageable
- above `10`: serious concern

### Outliers and influential observations

```r
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

data_nooutliers <- data_clean[outlier_df$outlier == 0, ]
```

Then rerun the same models on `data_nooutliers`.

### Random sampling

Usually qualitative in this course.

What to write:

- If sampling is not random, estimates may not generalize to the full population.
- This threatens external validity.

### Endogeneity

Usually qualitative in this course.

What to write:

- Possible sources: omitted variable bias, reverse causality, measurement error.
- If present, the coefficient may be biased and not causal.

## 7. Plug-and-play ggplot templates

### Scatterplot

```r
ggplot(data, aes(x = X_VAR, y = Y_VAR)) +
  geom_point(alpha = 0.7) +
  theme_minimal() +
  labs(
    title = "Scatterplot Title",
    x = "X-axis label",
    y = "Y-axis label"
  )
```

### Scatterplot with regression line

```r
ggplot(data, aes(x = X_VAR, y = Y_VAR)) +
  geom_point(alpha = 0.7) +
  geom_smooth(method = "lm", se = TRUE, color = "blue") +
  theme_minimal() +
  labs(
    title = "Regression Plot",
    x = "X-axis label",
    y = "Y-axis label"
  )
```

### Histogram

```r
ggplot(data, aes(x = X_VAR)) +
  geom_histogram(binwidth = 1, fill = "skyblue", color = "black") +
  theme_minimal() +
  labs(
    title = "Histogram Title",
    x = "Variable",
    y = "Count"
  )
```

### Boxplot by group

```r
ggplot(data, aes(x = factor(GROUP_VAR), y = Y_VAR, fill = factor(GROUP_VAR))) +
  geom_boxplot() +
  theme_minimal() +
  labs(
    title = "Boxplot Title",
    x = "Group",
    y = "Outcome"
  )
```

### Line plot over time

```r
ggplot(data, aes(x = YEAR_VAR, y = Y_VAR, color = GROUP_VAR)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  theme_minimal() +
  labs(
    title = "Trend Plot",
    x = "Year",
    y = "Outcome",
    color = "Group"
  )
```

### Coefficient or predicted-value plot from interaction model

```r
pred_df <- ggpredict(model_int, terms = c("X_VAR", "GROUP_VAR"))

ggplot(pred_df, aes(x = x, y = predicted, color = group)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  geom_ribbon(aes(ymin = conf.low, ymax = conf.high, fill = group), alpha = 0.15, color = NA) +
  theme_minimal() +
  labs(
    title = "Predicted Values from Interaction Model",
    x = "X variable",
    y = "Predicted outcome",
    color = "Group",
    fill = "Group"
  )
```

## 8. Safe exam workflow

Use this order unless the prompt clearly requires something else:

1. Load packages and data.
2. Run `str()` and `summary()`.
3. Clean missing values and convert types.
4. Merge only after making keys the same type.
5. Create transformed variables with `mutate()`.
6. Make one basic plot.
7. Run a bivariate model.
8. Add controls one at a time.
9. Report robust HC1 standard errors.
10. Check residual plot, `vif()`, and `bptest()`.
11. If needed, run a robustness check without outliers.
12. If the prompt asks whether effects differ by group or time, run an interaction model.

## 9. What to say in plain English

Useful sentence starters:

- "The coefficient on `X_VAR` is positive/negative, meaning that as `X_VAR` increases, `Y_VAR` tends to increase/decrease."
- "This association is statistically significant at conventional levels."
- "After adding controls, the magnitude becomes larger/smaller, suggesting potential confounding."
- "Because heteroskedasticity is a concern, I report HC1 robust standard errors."
- "The residual plot does/does not suggest major nonlinearity."
- "The VIF values do/do not suggest serious multicollinearity."
- "This result should be interpreted cautiously because endogeneity and non-random sampling cannot be ruled out."

