# Week 6 Lab Script: Diagnosing Violations of the Gauss-Markov Assumptions in Multiple Regression
# GPCO 454 - Quantitative Methods II (QM2)
# Author: Nico Ravanilla and David L. Vargas
# Date: February 13, 2026

# Install and load necessary packages
# install.packages("car")  # For diagnostic plots and VIF
# install..packages("ICSNP") # For Hotelling's T^2 test
# install.packages("knitr") # For nice tables
# install.packages("dplyr") # For data manipulation

# =============================================================================
# A. Linearity of the Model in Parameters (Case Study: COVID-19 Positivity Rate)
# =============================================================================

# 1. Simulating a dataset with *nonlinear* relationship -----------------------
set.seed(123)   # For reproducibility
N <- 100        # Number of counties

# Predictors
population_density <- rnorm(N, mean = 500, sd = 100)
average_income     <- rnorm(N, mean = 50000, sd = 10000)

#You created a variable! 
hist(population_density)
hist(average_income)

# Outcome: positivity_rate -- includes a quadratic term in population_density
# True data-generating process (DGP):
# positivity_rate = 20 + 0.002*(population_density^2)
#                   - 0.00015*(average_income) + random noise
positivity_rate <- 20 +
  0.002 * (population_density^2) -
  0.00015 * average_income +
  rnorm(N, mean = 0, sd = 3)

hist(positivity_rate)

# Combine into a data frame
covid_data <- data.frame(
  population_density,
  average_income,
  positivity_rate
)

#Quickly check the plot of covid and population density
plot(positivity_rate, population_density)

# Inspect the first few rows
head(covid_data)
summary(covid_data)

# 2. Fitting a (mis-specified) linear model -----------------------------------
# The data is truly quadratic in population_density, but we omit the squared term
model_covid_misspec <- lm(
  positivity_rate ~ population_density + average_income,
  data = covid_data
)

# Examine summary of mis-specified model
summary(model_covid_misspec)

library(stargazer)

stargazer(
  model_covid_misspec,
  type = "text",
  title = "Regression Results: Effects of Population Density on COVID Positivity",
  dep.var.labels = "COVID Positivity",
  covariate.labels = c(
    "Population Density",
    "Average Income"
  ),
  align = TRUE,
  no.space = TRUE,
  digits = 2
)

# 3. Diagnostic checks for nonlinearity ---------------------------------------
# 3a. Residual vs. Fitted Plot (Base R)
plot(model_covid_misspec, which = 1)

# 3b. Partial Residual Plots (from the car package)
#    install.packages("car") if not already installed
library(car)
avPlots(model_covid_misspec)

# Interpretation of mis-specified model diagnostics:
# - Look for a curved pattern in the residual vs. fitted plot.
# - A "U-shape" or inverted "U-shape" suggests a missing nonlinear term.
# - Partial residual plots (avPlots) can also reveal unmodeled curvature.

# 4. Correcting the nonlinearity ----------------------------------------------
# We add a quadratic term to properly capture the nonlinear effect:
model_covid_poly <- lm(
  positivity_rate ~ population_density + I(population_density^2) + average_income,
  data = covid_data
)

summary(model_covid_poly)

stargazer(
  model_covid_poly,
  type = "text",
  title = "Regression Results: Effects of Population Density on COVID Positivity",
  dep.var.labels = "COVID Positivity",
  covariate.labels = c(
    "Population Density",
    "Population Density Squared",
    "Average Income"
  ),
  align = TRUE,
  no.space = TRUE,
  digits = 2
)

# Compare diagnostics again for the corrected model
plot(model_covid_poly, which = 1)
avPlots(model_covid_poly)

# Interpretation of corrected model diagnostics:
# - If properly specified, residuals should scatter more randomly (no distinct curve).
# - Partial residual plots should not exhibit a pronounced bend for population_density.
#
# By including the quadratic term, we satisfy the linearity-in-parameters assumption.
# In practice, domain knowledge should guide which transformations or polynomials
# to add when detecting nonlinearity.


# =============================================================================
# B. Random Sampling
# (Case Study: Comparing Random vs. Biased Samples Against Known Population)
# =============================================================================

# 1. Create a simulated 'population' of 50,000 individuals with 5 variables ----
set.seed(1001)
pop_size <- 50000

monthly_housing_cost <- rnorm(pop_size, mean = 1500, sd = 300)
household_income     <- rnorm(pop_size, mean = 65000, sd = 15000)
age                  <- rnorm(pop_size, mean = 40, sd = 10)
household_size       <- rpois(pop_size, lambda = 2)
education_years      <- rnorm(pop_size, mean = 14, sd = 2)

population_data <- data.frame(
  monthly_housing_cost,
  household_income,
  age,
  household_size,
  education_years
)

# Calculate the "true" population means (since we generated the data)
pop_means <- colMeans(population_data)

cat("Population size:", nrow(population_data), "\n")
cat("True Population Means:\n")
print(pop_means)

# 2. Draw a truly random sample of 200 -----------------------------------------
sample_size <- 200
rand_idx <- sample(nrow(population_data), sample_size)
random_sample <- population_data[rand_idx, ]

cat("\n--- Random Sample Means ---\n")
print(colMeans(random_sample))

# 3. Construct a biased sample (oversampling high-cost, high-income) -----------
biased_subset <- subset(
  population_data,
  monthly_housing_cost > 1800 & household_income > 70000
)
biased_idx <- sample(nrow(biased_subset), sample_size)
biased_sample <- biased_subset[biased_idx, ]

cat("\n--- Biased Sample Means ---\n")
print(colMeans(biased_sample))

# 4. Univariate t-tests comparing sample means to population means -------------
cat("\n=== Univariate t-tests: Random Sample vs. Population Means ===\n")
for (var_name in names(random_sample)) {
  cat("\nVariable:", var_name, "\n")
  print(
    t.test(random_sample[[var_name]], mu = pop_means[var_name])
  )
}

cat("\n=== Univariate t-tests: Biased Sample vs. Population Means ===\n")
for (var_name in names(biased_sample)) {
  cat("\nVariable:", var_name, "\n")
  print(
    t.test(biased_sample[[var_name]], mu = pop_means[var_name])
  )
}

# 5. Multivariate test (Hotelling's T^2) for joint mean equality ---------------
# install.packages("ICSNP") # if not already installed
library(ICSNP)

# Convert data frames to matrices
random_sample_mat <- as.matrix(random_sample)
biased_sample_mat <- as.matrix(biased_sample)

cat("\n=== Hotelling's T^2 for Random Sample ===\n")
ht2_random <- HotellingsT2(random_sample_mat, mu = pop_means)
print(ht2_random)

cat("\n=== Hotelling's T^2 for Biased Sample ===\n")
ht2_biased <- HotellingsT2(biased_sample_mat, mu = pop_means)
print(ht2_biased)

# Interpretation:
# - If random_sample is truly representative, we expect minimal (or no) significant
#   differences from the population means (univariate t-tests) and non-rejection
#   of Hotelling's T^2.
# - For biased_sample, we should see significant differences in 'monthly_housing_cost'
#   and 'household_income' at least, and likely a rejection of joint equality
#   across all variables.

# -----------------------------------------------------------------------------
# Saving T-Test Results in a Nice Table
# -----------------------------------------------------------------------------

# (1) Make sure you have the knitr and dplyr packages installed
# install.packages("knitr")
# install.packages("dplyr")

library(knitr)
library(dplyr)

# Assume the following objects already exist in your environment:
#  - population_data: Data frame of population
#  - pop_means: Named numeric vector of population means
#  - random_sample: Data frame (truly random sample)
#  - biased_sample: Data frame (biased sample)

# --- Function to run one-sample t-tests against known pop_means and store results
capture_ttests <- function(sample_df, pop_means_vec) {
  result_list <- lapply(names(sample_df), function(var_name) {
    test_out <- t.test(sample_df[[var_name]], mu = pop_means_vec[var_name])
    data.frame(
      variable    = var_name,
      pop_mean    = pop_means_vec[var_name],
      sample_mean = mean(sample_df[[var_name]]),
      difference  = mean(sample_df[[var_name]]) - pop_means_vec[var_name],
      conf_lower  = test_out$conf.int[1],
      conf_upper  = test_out$conf.int[2],
      p_value     = test_out$p.value
    )
  })
  bind_rows(result_list)
}

# --- (2) Capture results for the random sample
random_results <- capture_ttests(random_sample, pop_means)

# --- (3) Capture results for the biased sample
biased_results <- capture_ttests(biased_sample, pop_means)

# --- (4) Print out the results in a nice table format
cat("\n=== Random Sample T-Test Results ===\n")
kable(random_results, digits = 3)

cat("\n=== Biased Sample T-Test Results ===\n")
kable(biased_results, digits = 3)


# =============================================================================
# C. Multicollinearity: Diagnosing via Variance Inflation Factors (VIF)
# (Case Study: Wage Determinants)
# =============================================================================

set.seed(42)  # Ensures reproducibility
N <- 5000  # Number of individuals

age <- rnorm(N, mean = 40, sd = 10)  # Age is normally distributed around 40

years_of_experience <- age - 18 + rnorm(N, mean = 0, sd = 2)  
# Experience = Age - Schooling Start Age (18) + Some Noise
years_of_education <- rnorm(N, mean = 14, sd = 2)  # Education: Avg. 14 years ± 2

monthly_wage <- 2000 +  
  100 * years_of_education +  
  300 * years_of_experience +  
  rnorm(N, mean = 0, sd = 500)  # Adds random noise

wage_data <- data.frame(
  monthly_wage,
  age,
  years_of_education,
  years_of_experience
)

# --------------------
# 1. Initial Model with Potential Multicollinearity
# --------------------
cat("\n=== Initial Model (Potential Collinearity) ===\n")

model_wage1 <- lm(
  monthly_wage ~ age + years_of_education + years_of_experience,
  data = wage_data
)

cat("\n--- Model Summary (model_wage1) ---\n")
summary(model_wage1)

# Compute Variance Inflation Factors for model_wage1
# install.packages("car")  # if not installed
library(car)

cat("\n--- VIF (model_wage1) ---\n")
vif_values1 <- vif(model_wage1)
print(vif_values1)

# Interpretation:
# If 'age' and 'years_of_experience' are strongly correlated, 
# we may see inflated VIF values for these predictors.

# --------------------
# 2. Correcting the Model by Dropping a Redundant Variable
# --------------------
# For demonstration, we drop 'age' and keep 'years_of_experience',
# assuming it's more relevant for explaining wages.

cat("\n=== Corrected Model (Dropping 'age') ===\n")

model_wage2 <- lm(
  monthly_wage ~ years_of_education + years_of_experience,
  data = wage_data
)

cat("\n--- Model Summary (model_wage2) ---\n")
summary(model_wage2)

# Re-check VIFs
cat("\n--- VIF (model_wage2) ---\n")
vif_values2 <- vif(model_wage2)
print(vif_values2)

# Interpretation:
# - If VIF values drop to more acceptable levels (e.g., <5), 
#   we've reduced the severity of multicollinearity.
# - In practice, also consider theoretical importance of each variable.

