# Week 3 Lab Script: Cleaning Data, Transformations, and Multiple Regression
# GPCO 454 - Quantitative Methods II (QM2)

# ==========================================================
# 1. Preparing, Cleaning, and Organizing Data
# ==========================================================

# NEW! Cleaning the enviroment before running the script
rm(list = ls())

# Set working directory
setwd('/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/R Studio/3')
getwd()

# Load the necessary packages
library(tidyverse)
library(readxl)
library(stargazer)
library(ggplot2)

# Load the dataset
class_survey <- read_excel("class baseline survey.xlsx")

# Create the 'age' variable
class_survey <- class_survey %>%
  mutate(age = case_when(
    age_group == "18 - 20" ~ 19,
    age_group == "21 - 23" ~ 22,
    age_group == "24 - 26" ~ 25,
    age_group == "27 - 29" ~ 28,
    age_group == "30 - 32" ~ 31,
    age_group == "33 - 35" ~ 34,
    age_group == "36 - 38" ~ 37,
    age_group == "39 - 41" ~ 40,
    age_group == "42 - 44" ~ 43,
    age_group == "48 - 50" ~ 49,
    age_group == "Prefer not to say" ~ NA_real_,
    TRUE ~ NA_real_
  ))

# Create a binary variable for female
class_survey <- class_survey %>%
  mutate(female = case_when(
    gender == "Female" ~ 1,
    gender == "Male" ~ 0,
    gender == "Prefer not to say" | is.na(gender) ~ NA_real_,
    TRUE ~ NA_real_
  ))

# Recode the 'international' variable
class_survey <- class_survey %>%
  mutate(international = case_when(
    international == "Yes" ~ 1,
    international == "No" ~ 0,
    international == "Prefer not to say" | is.na(international) ~ NA_real_,
    TRUE ~ NA_real_
  ))

# Create binary indicator variables for education categories
class_survey <- class_survey %>%
  mutate(
    educ = ifelse(educ == "", NA_character_, educ),
    educ_socsci = case_when(
      educ == "Primarily Social Sciences (e.g., economics, political science, sociology)" ~ 1,
      educ == "Prefer not to say" | is.na(educ) ~ NA_real_,
      TRUE ~ 0
    ),
    educ_hum = case_when(
      educ == "Primarily Humanities (e.g., literature, philosophy, history)" ~ 1,
      educ == "Prefer not to say" | is.na(educ) ~ NA_real_,
      TRUE ~ 0
    ),
    educ_stem = case_when(
      educ == "Primarily STEM (e.g., science, technology, engineering, mathematics)" ~ 1,
      educ == "Prefer not to say" | is.na(educ) ~ NA_real_,
      TRUE ~ 0
    ),
    educ_other = case_when(
      educ == "Other:" ~ 1,
      educ == "Prefer not to say" | is.na(educ) ~ NA_real_,
      TRUE ~ 0
    )
  )

# Transform salary into numeric income variable (in thousands of dollars)
class_survey <- class_survey %>%
  mutate(
    income = case_when(
      salary == "$100,000 - $124,999" ~ 112.5,
      salary == "$125,000 - $199,999" ~ 162.5,
      salary == "$20,000 - $39,999" ~ 30,
      salary == "$40,000 - $59,999" ~ 50,
      salary == "$60,000 - $79,999" ~ 70,
      salary == "$80,000 - $99,999" ~ 90,
      salary == "Less than $20,000" ~ 20,
      salary == "Never worked" ~ 0,
      salary == "Prefer not to say" | salary == "" | is.na(salary) ~ NA_real_,
      TRUE ~ NA_real_
    )
  )

# Ensure years_at_school and years_at_work are numeric
class_survey <- class_survey %>%
  mutate(
    years_at_school = case_when(
      years_at_school == "Prefer not to say" | years_at_school == "" ~ NA_real_, #replaces thing with missing values
      TRUE ~ as.numeric(years_at_school) #delcares to R that this is numeric 
    ),
    years_at_work = case_when(
      years_at_work == "Prefer not to say" | years_at_work == "" ~ NA_real_,
      TRUE ~ as.numeric(years_at_work)
    )
  )

# Transform income into log(1 + income)
class_survey <- class_survey %>%
  mutate(log_income = log(1 + income))

# ==========================================================
# 2. Examining the Data
# ==========================================================

# Generate histogram of years_at_school
ggplot(class_survey, aes(x = years_at_school)) +
  geom_histogram(binwidth = 1, fill = "blue", alpha = 0.6, color = "black") +
  labs(
    title = "Histogram of Years at School",
    x = "Years at School",
    y = "Count"
  ) +
  theme_minimal()

# Generate histogram of years_at_work
ggplot(class_survey, aes(x = years_at_work)) +
  geom_histogram(binwidth = 1, fill = "blue", alpha = 0.6, color = "black") +
  labs(
    title = "Histogram of Years of Experience",
    x = "Years of Experience",
    y = "Count"
  ) +
  theme_minimal()

# Generate histogram of income
ggplot(class_survey, aes(x = income)) +
  geom_histogram(binwidth = 10, fill = "blue", alpha = 0.6, color = "black") +
  scale_x_continuous(
    limits = range(class_survey$income, na.rm = TRUE),
    breaks = seq(0, max(class_survey$income, na.rm = TRUE), by = 20)
  ) +
  labs(
    title = "Histogram of Income",
    x = "Income",
    y = "Count"
  ) +
  theme_minimal()

# ==========================================================
# 3. Running Your First Multiple Regression
# ==========================================================

# Bivariate regression of log_income on years_at_school
model_00 <- lm(log_income ~ years_at_school, data = class_survey)
summary(model_00)

# Multiple regression with experience and demographic controls
class_survey <- class_survey %>% 
  mutate(years_at_work_squared = years_at_work^2)

model_0 <- lm(log_income ~ years_at_school + years_at_work + years_at_work_squared, data = class_survey)
model_1 <- lm(log_income ~ years_at_school + years_at_work + years_at_work_squared + age, data = class_survey)
model_2 <- lm(log_income ~ years_at_school + years_at_work + years_at_work_squared + age + female, data = class_survey)
model_3 <- lm(log_income ~ years_at_school + years_at_work + years_at_work_squared + age + female + international, data = class_survey)
model_4 <- lm(log_income ~ years_at_school + years_at_work + years_at_work_squared + age + female + international +
                educ_socsci + educ_hum + educ_stem + educ_other, data = class_survey)

# Summarize all models
stargazer(
  model_00, model_0, model_1, model_2, model_3, model_4,
  type = "text",
  title = "Regression Table",
  align = TRUE,
  dep.var.labels = "Log(1 + Income)",
  covariate.labels = c(
    "Years at School", "Years at Work", "Years at Work Squared",
    "Age", "Female", "International",
    "Education: Social Sciences", "Education: Humanities",
    "Education: STEM", "Education: Other"
  ),
  omit.stat = c("f", "ser"),
  notes = "Dependent variable is Log(1 + Income).",
  out = "regression_table.txt"
)

# ==========================================================
# 4. Visualizing Regression Coefficients
# ==========================================================

# Plot regression coefficients for years_at_school
library(broom)
coeff_data <- do.call(rbind, lapply(list(model_00, model_0, model_1, model_2, model_3, model_4), function(model) {
  tidy(model, conf.int = TRUE) %>%
    filter(term == "years_at_school")
}))
coeff_data$model <- c("Model 1", "Model 2", "Model 3", "Model 4", "Model 5", "Model 6")

ggplot(coeff_data, aes(x = model, y = estimate)) +
  geom_point(size = 3) +
  geom_errorbar(aes(ymin = conf.low, ymax = conf.high), width = 0.2) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
  labs(
    title = "Effect of Years at School on Log(1 + Income) Across Models",
    x = "Model",
    y = "Coefficient Estimate (with 95% CI)"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave("years_at_school_coefficients.png", width = 8, height = 6)
