################################################################################
# GPEC 446 - Quantitative Methods 3 (Valasquez)
# Homework 2: Panel and Regression Discontinuity
# Edgar Agunias - May 2026
#
# This script runs the complete statistical analysis for Homework 2 from start to
# finish. It is structured sequentially without custom helper functions to keep the
# workflow completely simple, transparent, and reproducible.
################################################################################

# ==============================================================================
# SECTION 0: Setup and Package Loading
# ==============================================================================

# Set the working directory to the current Homework 2 copy folder.
# This ensures all file reads and writes use clean relative paths.
setwd("/Users/edgar/Documents/000 Files/02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez/Assignments/Homework 2 copy")

# Load core packages for data cleaning, regression tables, Stata file import,
# plotting, and robust regression discontinuity estimation.
library(dplyr)
library(ggplot2)
library(jsonlite)
library(broom)
library(stargazer)
library(haven)
library(rdrobust)

# ==============================================================================
# SECTION 1: Part I Data Cleaning and Merging (World Bank Join)
# ==============================================================================

# Step 1.1: Load the professor-provided Africa panel database.
# This loads a data frame named 'Africa_GDP' with 967 rows and 5 columns:
# country, year, pol_lib, bigimp, and an empty or placeholder GDP field.
load("Africa_GDP.Rda")

# Step 1.2: Define the homework's analysis timeframe.
analysis_years <- 1985:1998

# Step 1.3: Define a robust mapping table to resolve name differences
# between our dataset's countries and the official World Bank API names.
# Key corrections: Cape Verde is "Cabo Verde" and Swaziland is "Eswatini".
country_lookup <- tibble::tibble(
  country = sort(unique(Africa_GDP$country)),
  wb_name = c(
    "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon",
    "Cabo Verde", "Central African Republic", "Chad", "Comoros",
    "Congo, Dem. Rep.", "Congo, Rep.", "Cote d'Ivoire", "Eritrea",
    "Ethiopia", "Gabon", "Gambia, The", "Ghana", "Guinea",
    "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Madagascar",
    "Malawi", "Mali", "Mauritania", "Mauritius", "Mozambique",
    "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe",
    "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa",
    "Sudan", "Eswatini", "Tanzania", "Togo", "Uganda", "Zambia",
    "Zimbabwe"
  )
)

# Step 1.4: Fetch constant GDP per Capita (constant 2015 USD) from the World Bank API.
# Indicator: NY.GDP.PCAP.KD (GDP per capita in constant 2015 US dollars)
# We fetch all countries for our analysis years (1985 to 1998) in a single JSON call.
gdp_pc_url <- paste0(
  "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.KD",
  "?format=json&date=", min(analysis_years), ":", max(analysis_years),
  "&per_page=20000"
)

gdp_pc_raw <- jsonlite::fromJSON(gdp_pc_url)

# Stop the script if the World Bank API returns an error or invalid structure.
if (length(gdp_pc_raw) < 2 || !is.data.frame(gdp_pc_raw[[2]])) {
  stop("Error: World Bank API did not return a valid data frame for GDP per capita.")
}

# Keep and rename the key columns from the raw GDP data frame.
gdp_pc_wb <- gdp_pc_raw[[2]] %>%
  transmute(
    wb_name = .data$country$value,
    iso3 = .data$countryiso3code,
    year = as.integer(.data$date),
    gdp_pc_constant_usd = as.numeric(.data$value)
  )

# Step 1.5: Fetch Total Population from the World Bank API.
# Indicator: SP.POP.TOTL (Total Population)
# Used as weight in Question 4 to estimate representative-person parameters.
pop_url <- paste0(
  "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL",
  "?format=json&date=", min(analysis_years), ":", max(analysis_years),
  "&per_page=20000"
)

pop_raw <- jsonlite::fromJSON(pop_url)

# Stop the script if the World Bank API returns an error or invalid structure.
if (length(pop_raw) < 2 || !is.data.frame(pop_raw[[2]])) {
  stop("Error: World Bank API did not return a valid data frame for population.")
}

# Keep and rename the key columns from the raw population data frame.
pop_wb <- pop_raw[[2]] %>%
  transmute(
    wb_name = .data$country$value,
    iso3 = .data$countryiso3code,
    year = as.integer(.data$date),
    population = as.numeric(.data$value)
  )

# Step 1.6: Merge WDI indicators with our main Africa panel.
panel <- Africa_GDP %>%
  # Filter the panel to only keep the 1985-1998 homework years.
  filter(year %in% analysis_years) %>%
  # Join our country mapping lookup table.
  left_join(country_lookup, by = "country") %>%
  # Join World Bank GDP per capita by country name and year.
  left_join(gdp_pc_wb, by = c("wb_name", "year")) %>%
  # Join World Bank Population by country name, year, and ISO3 code.
  left_join(pop_wb, by = c("wb_name", "year", "iso3")) %>%
  # Sort chronologically by country and year.
  arrange(country, year) %>%
  # Create a unique country factor ID, a year factor, and fill NA bigimp values with 0.
  mutate(
    country_id = as.integer(factor(country, levels = sort(unique(country)))),
    year_factor = factor(year),
    bigimp = ifelse(is.na(bigimp), 0, bigimp)
  ) %>%
  # Identify each country's "big improvement" year and calculate relative event-time (leadlag).
  group_by(country) %>%
  mutate(
    # event_year is the year where bigimp == 1 (if the country had an improvement).
    event_year = ifelse(any(bigimp == 1, na.rm = TRUE), year[which.max(bigimp)], NA_integer_),
    # leadlag is the number of years relative to the improvement year.
    leadlag = ifelse(!is.na(event_year), year - event_year, NA_integer_)
  ) %>%
  ungroup()

# Step 1.7: Keep only complete cases (observations with non-missing GDP and governance) for regressions.
complete_panel <- panel %>%
  filter(!is.na(pol_lib), !is.na(gdp_pc_constant_usd))

# ==============================================================================
# SECTION 2: Part I, Question 1 - Pooled OLS vs. Country Fixed Effects
# ==============================================================================

# Run a pooled OLS regression of constant GDP per capita on political liberties,
# controlling for year fixed effects.
pooled_ols <- lm(gdp_pc_constant_usd ~ pol_lib + year_factor, data = complete_panel)

# Run a country fixed-effects model (LSDV method) of constant GDP per capita
# on political liberties, controlling for country and year fixed effects.
within_lsdv <- lm(gdp_pc_constant_usd ~ pol_lib + factor(country_id) + year_factor, data = complete_panel)

# Export the regression outputs to a professional HTML table file.
stargazer(
  pooled_ols,
  within_lsdv,
  type = "html",
  omit.stat = c("f", "ser"),
  digits = 3,
  title = "Table 1. GDP per Capita and Political Liberties, Average-Country Estimates",
  dep.var.labels = "GDP per capita (constant 2015 USD)",
  column.labels = c("Pooled OLS + year FE", "Country FE + year FE"),
  covariate.labels = "Political liberties (RHS)",
  keep = "pol_lib",
  out = "table_q1_pooled_within.html"
)

# ==============================================================================
# SECTION 3: Part I, Question 2 - Two-Way Fixed Effects (TWFE) & Event Study
# ==============================================================================

# Step 3.1: Run a static TWFE regression of constant GDP per capita on the bigimp dummy,
# controlling for country and year fixed effects.
twfe_bigimp <- lm(gdp_pc_constant_usd ~ bigimp + factor(country_id) + year_factor, data = complete_panel)

# Export the static TWFE regression output to a professional HTML table file.
stargazer(
  twfe_bigimp,
  type = "html",
  omit.stat = c("f", "ser"),
  digits = 3,
  title = "Table 2. TWFE Estimate for Large Governance Improvement Year",
  dep.var.labels = "GDP per capita (constant 2015 USD)",
  covariate.labels = "Big governance improvement year",
  keep = "bigimp",
  out = "table_q2_twfe_bigimp.html"
)

# Step 3.2: Estimate the dynamic event-study coefficients.
# We keep observations in the [-5, +5] event window and use year -1 as the omitted reference.
event_data <- complete_panel %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5) %>%
  mutate(leadlag_f = relevel(factor(leadlag), ref = "-1"))

event_study_model <- lm(
  gdp_pc_constant_usd ~ leadlag_f + factor(country_id) + year_factor,
  data = event_data
)

# Extract only the event-time dummy coefficients and calculate their 95% confidence intervals.
event_coef_table <- broom::tidy(event_study_model) %>%
  filter(grepl("^leadlag_f", term)) %>%
  transmute(
    leadlag = as.integer(sub("^leadlag_f", "", term)),
    estimate,
    std_error = std.error,
    statistic,
    p_value = p.value,
    ci_low = estimate - 1.96 * std_error,
    ci_high = estimate + 1.96 * std_error
  )

# Add the omitted reference period (year -1) back into the dataset with values set to zero.
event_coef_plot_data <- bind_rows(
  event_coef_table,
  tibble::tibble(
    leadlag = -1, estimate = 0, std_error = 0, statistic = NA_real_,
    p_value = NA_real_, ci_low = 0, ci_high = 0
  )
) %>%
  arrange(leadlag)

# Export the event-study coefficients to an HTML table.
stargazer(
  as.data.frame(event_coef_plot_data),
  type = "html",
  summary = FALSE,
  rownames = FALSE,
  title = "Event-Study Lead/Lag Coefficients",
  digits = 3,
  out = "event_study_leadlag_coefficients.html"
)

# Plot and save the event-study coefficient figure with 95% confidence intervals.
event_plot <- ggplot(event_coef_plot_data, aes(x = leadlag, y = estimate)) +
  geom_hline(yintercept = 0, color = "darkred", linewidth = 0.4, linetype = "dashed") +
  geom_vline(xintercept = -0.5, color = "steelblue", linewidth = 0.4, linetype = "dashed") +
  geom_errorbar(aes(ymin = ci_low, ymax = ci_high), width = 0.15, color = "gray35") +
  geom_point(color = "#1b4f72", size = 2) +
  scale_x_continuous(breaks = -5:5) +
  labs(
    title = "Event Study: GDP and Governance Improvements",
    subtitle = "TWFE event-time coefficients; reference period is year -1",
    x = "Years before/after largest political-liberty improvement",
    y = "Change in GDP per capita relative to year -1 (constant USD)"
  ) +
  theme_minimal(base_size = 12)

ggsave("figure_q2_event_study_coefficients.png", event_plot, width = 8, height = 5, dpi = 300)

# Step 3.3: Residual-based Event Study Diagnostic.
# We regress GDP per capita on country and year fixed effects only, and extract the residuals.
twfe_resid_model <- lm(gdp_pc_constant_usd ~ factor(country_id) + year_factor, data = complete_panel)

# Attach the residuals to the complete panel and keep the [-5, +5] event window.
residual_event_data <- complete_panel %>%
  mutate(twfe_residual = resid(twfe_resid_model)) %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5)

# Calculate the mean residual and 95% confidence intervals for each event year.
event_summary <- residual_event_data %>%
  group_by(leadlag) %>%
  summarise(
    mean_residual = mean(twfe_residual, na.rm = TRUE),
    se = sd(twfe_residual, na.rm = TRUE) / sqrt(dplyr::n()),
    n = dplyr::n(),
    .groups = "drop"
  ) %>%
  mutate(
    ci_low = mean_residual - 1.96 * se,
    ci_high = mean_residual + 1.96 * se
  )

# Export the event-study residual means to an HTML table.
stargazer(
  as.data.frame(event_summary),
  type = "html",
  summary = FALSE,
  rownames = FALSE,
  title = "Event-Study Residual Means",
  digits = 3,
  out = "event_study_residual_means.html"
)

# Plot and save the residual diagnostic event-study curve.
residual_event_plot <- ggplot(event_summary, aes(x = leadlag, y = mean_residual)) +
  geom_hline(yintercept = 0, color = "gray45", linewidth = 0.4) +
  geom_vline(xintercept = 0, color = "firebrick", linewidth = 0.4, linetype = "dashed") +
  geom_errorbar(aes(ymin = ci_low, ymax = ci_high), width = 0.15, color = "gray35") +
  geom_line(color = "#1b4f72", linewidth = 0.7) +
  geom_point(color = "#1b4f72", size = 2) +
  scale_x_continuous(breaks = -5:5) +
  labs(
    title = "GDP per Capita Residuals Around Largest Governance Improvement",
    subtitle = "Residuals after removing country and year fixed effects",
    x = "Years relative to largest political-liberty improvement",
    y = "Mean GDP per capita residual (constant USD)"
  ) +
  theme_minimal(base_size = 12)

ggsave("figure_q2_event_study_residuals.png", residual_event_plot, width = 8, height = 5, dpi = 300)

# ==============================================================================
# SECTION 4: Part I, Question 4 - Representative-Person (Weighted) Version
# ==============================================================================

# Keep country-year observations that have positive World Bank population values.
representative_person <- complete_panel %>%
  filter(!is.na(population), population > 0)

# Run population-weighted pooled OLS with year fixed effects.
weighted_pooled <- lm(
  gdp_pc_constant_usd ~ pol_lib + year_factor,
  data = representative_person,
  weights = population
)

# Run population-weighted country fixed effects with year fixed effects.
weighted_within <- lm(
  gdp_pc_constant_usd ~ pol_lib + factor(country_id) + year_factor,
  data = representative_person,
  weights = population
)

# Export the population-weighted regressions to a professional HTML table file.
stargazer(
  weighted_pooled,
  weighted_within,
  type = "html",
  omit.stat = c("f", "ser"),
  digits = 3,
  title = "Table 3. GDP per Capita and Political Liberties, Representative-Person Estimates",
  dep.var.labels = "GDP per capita (constant 2015 USD)",
  column.labels = c("Weighted pooled OLS + year FE", "Weighted country FE + year FE"),
  covariate.labels = "Political liberties (RHS)",
  keep = "pol_lib",
  out = "table_q4_representative_person.html"
)

# Estimate population-weighted residuals (removing country and year fixed effects).
weighted_resid_model <- lm(
  gdp_pc_constant_usd ~ factor(country_id) + year_factor,
  data = representative_person,
  weights = population
)

# Attach the weighted residuals to the dataset and keep the [-5, +5] event window.
weighted_event_data <- representative_person %>%
  mutate(weighted_twfe_residual = resid(weighted_resid_model)) %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5)

# Calculate the population-weighted mean residual for each event year.
weighted_event_summary <- weighted_event_data %>%
  group_by(leadlag) %>%
  summarise(
    weighted_mean_residual = weighted.mean(weighted_twfe_residual, w = population, na.rm = TRUE),
    total_population = sum(population, na.rm = TRUE),
    country_years = dplyr::n(),
    .groups = "drop"
  )

# Export the population-weighted event-study residual table.
stargazer(
  as.data.frame(weighted_event_summary),
  type = "html",
  summary = FALSE,
  rownames = FALSE,
  title = "Population-Weighted Event-Study Residual Means",
  digits = 3,
  out = "weighted_event_study_residual_means.html"
)

# Plot and save the population-weighted event-study residual diagram.
weighted_event_plot <- ggplot(weighted_event_summary, aes(x = leadlag, y = weighted_mean_residual)) +
  geom_hline(yintercept = 0, color = "gray45", linewidth = 0.4) +
  geom_vline(xintercept = 0, color = "firebrick", linewidth = 0.4, linetype = "dashed") +
  geom_line(color = "#7d3c98", linewidth = 0.7) +
  geom_point(color = "#7d3c98", size = 2) +
  scale_x_continuous(breaks = -5:5) +
  labs(
    title = "Population-Weighted GDP Residuals Around Governance Improvement",
    subtitle = "Representative-person version using World Bank population weights",
    x = "Years relative to largest political-liberty improvement",
    y = "Population-weighted mean GDP per capita residual (constant USD)"
  ) +
  theme_minimal(base_size = 12)

ggsave("figure_q4_weighted_event_study_residuals.png", weighted_event_plot, width = 8, height = 5, dpi = 300)

# ==============================================================================
# SECTION 5: Part II Data Preparation (Angrist & Lavy RDD)
# ==============================================================================

# Load fifth-grade school-level data from the Stata format.
grade5 <- haven::read_dta("grade5.dta")

# Define the Maimonides' Rule enrollment cutoff.
cutoff <- 40

# Define the sample restriction: schools with fewer than 80 students enrolled.
max_enrollment <- 80

# Define the manual local linear bandwidth (10 students).
manual_bw <- 10

# Create key analysis variables: centered enrollment and the above-cutoff indicator.
analysis <- grade5 %>%
  transmute(
    schlcode = as.integer(schlcode),
    school_enrollment = as.numeric(school_enrollment),
    classize = as.numeric(classize),
    avgmath = as.numeric(avgmath),
    avgverb = as.numeric(avgverb),
    disadvantaged = as.numeric(disadvantaged),
    female = as.numeric(female),
    religious = as.numeric(religious),
    # Center the running variable (school_enrollment) around the cutoff of 40.
    enrollment_centered = school_enrollment - cutoff,
    # Indicator dummy equal to 1 if school enrollment is at or above 40.
    above_cutoff = as.integer(school_enrollment >= cutoff)
  )

# Keep the standard RDD subsample: schools with under 80 students enrolled.
analysis_under80 <- analysis %>%
  filter(school_enrollment < max_enrollment)

# ==============================================================================
# SECTION 6: Part II, Question 6 - Histogram of the Running Variable
# ==============================================================================

# Create a school-level enrollment histogram to test for strategic bunching.
hist_school_enrollment_plot <- ggplot(analysis, aes(x = school_enrollment)) +
  geom_histogram(binwidth = 5, boundary = 0, color = "white", fill = "#4C78A8") +
  geom_vline(xintercept = cutoff, color = "#C44E52", linewidth = 1, linetype = "dashed") +
  labs(
    title = "Distribution of Fifth-Grade School Enrollment",
    subtitle = "Dashed line marks the Maimonides' Rule cutoff at 40 students",
    x = "School enrollment",
    y = "Number of schools"
  ) +
  theme_minimal(base_size = 12)

ggsave("hist_school_enrollment.png", hist_school_enrollment_plot, width = 8, height = 5, dpi = 300)

# ==============================================================================
# SECTION 7: Part II, Question 7 - RDD Descriptive Plots
# ==============================================================================

# Create first-stage and reduced-form plots around the cutoff of 40.
# We plot individual school dots (in light gray), school enrollment bin averages
# (in green), and separate linear regression fits on each side of the cutoff.

# Step 7.1: Class Size (First Stage)
classize_bin <- analysis_under80 %>%
  group_by(school_enrollment) %>%
  summarise(mean_outcome = mean(classize, na.rm = TRUE), .groups = "drop")

rdd_classize_plot <- ggplot(analysis_under80, aes(x = school_enrollment, y = classize)) +
  geom_point(alpha = 0.15, color = "#4D4D4D", size = 1.1) +
  geom_point(data = classize_bin, aes(y = mean_outcome), color = "#1B9E77", size = 2) +
  geom_smooth(data = filter(analysis_under80, school_enrollment < cutoff), method = "lm", formula = y ~ x, color = "#1F77B4") +
  geom_smooth(data = filter(analysis_under80, school_enrollment >= cutoff), method = "lm", formula = y ~ x, color = "#D62728") +
  geom_vline(xintercept = cutoff, color = "#C44E52", linewidth = 1, linetype = "dashed") +
  labs(
    title = "Class Size Around the Enrollment Cutoff",
    subtitle = "Schools with enrollment under 80; separate linear fits on each side of 40",
    x = "School enrollment",
    y = "Class size"
  ) +
  theme_minimal(base_size = 12)

ggsave("rdd_classize_cutoff40.png", rdd_classize_plot, width = 8, height = 5, dpi = 300)

# Step 7.2: Math Scores (Reduced Form)
avgmath_bin <- analysis_under80 %>%
  group_by(school_enrollment) %>%
  summarise(mean_outcome = mean(avgmath, na.rm = TRUE), .groups = "drop")

rdd_avgmath_plot <- ggplot(analysis_under80, aes(x = school_enrollment, y = avgmath)) +
  geom_point(alpha = 0.15, color = "#4D4D4D", size = 1.1) +
  geom_point(data = avgmath_bin, aes(y = mean_outcome), color = "#1B9E77", size = 2) +
  geom_smooth(data = filter(analysis_under80, school_enrollment < cutoff), method = "lm", formula = y ~ x, color = "#1F77B4") +
  geom_smooth(data = filter(analysis_under80, school_enrollment >= cutoff), method = "lm", formula = y ~ x, color = "#D62728") +
  geom_vline(xintercept = cutoff, color = "#C44E52", linewidth = 1, linetype = "dashed") +
  labs(
    title = "Average Math Score Around the Enrollment Cutoff",
    subtitle = "Schools with enrollment under 80; separate linear fits on each side of 40",
    x = "School enrollment",
    y = "Average math score"
  ) +
  theme_minimal(base_size = 12)

ggsave("rdd_avgmath_cutoff40.png", rdd_avgmath_plot, width = 8, height = 5, dpi = 300)

# Step 7.3: Verbal Scores (Reduced Form)
avgverb_bin <- analysis_under80 %>%
  group_by(school_enrollment) %>%
  summarise(mean_outcome = mean(avgverb, na.rm = TRUE), .groups = "drop")

rdd_avgverb_plot <- ggplot(analysis_under80, aes(x = school_enrollment, y = avgverb)) +
  geom_point(alpha = 0.15, color = "#4D4D4D", size = 1.1) +
  geom_point(data = avgverb_bin, aes(y = mean_outcome), color = "#1B9E77", size = 2) +
  geom_smooth(data = filter(analysis_under80, school_enrollment < cutoff), method = "lm", formula = y ~ x, color = "#1F77B4") +
  geom_smooth(data = filter(analysis_under80, school_enrollment >= cutoff), method = "lm", formula = y ~ x, color = "#D62728") +
  geom_vline(xintercept = cutoff, color = "#C44E52", linewidth = 1, linetype = "dashed") +
  labs(
    title = "Average Verbal Score Around the Enrollment Cutoff",
    subtitle = "Schools with enrollment under 80; separate linear fits on each side of 40",
    x = "School enrollment",
    y = "Average verbal score"
  ) +
  theme_minimal(base_size = 12)

ggsave("rdd_avgverb_cutoff40.png", rdd_avgverb_plot, width = 8, height = 5, dpi = 300)

# ==============================================================================
# SECTION 8: Part II, Question 8a - Manual Local Linear RDD (Bandwidth = 10)
# ==============================================================================

# We implement a local linear regression: Outcome ~ above_cutoff + enrollment_centered + above_cutoff * enrollment_centered
# for observations within 10 units of the cutoff (enrollment between 30 and 50).

# Step 8.1: Manual local linear for Math Scores
math_manual_win <- analysis_under80 %>%
  filter(abs(school_enrollment - cutoff) <= manual_bw) %>%
  filter(!is.na(avgmath), !is.na(school_enrollment), !is.na(above_cutoff))

math_fit <- lm(avgmath ~ above_cutoff * enrollment_centered, data = math_manual_win)
math_coefs <- summary(math_fit)$coefficients

math_manual_res <- tibble::tibble(
  outcome = "avgmath",
  cutoff = cutoff,
  bandwidth = manual_bw,
  estimate = math_coefs["above_cutoff", "Estimate"],
  std_error = math_coefs["above_cutoff", "Std. Error"],
  p_value = math_coefs["above_cutoff", "Pr(>|t|)"],
  n_left = sum(math_manual_win$school_enrollment < cutoff),
  n_right = sum(math_manual_win$school_enrollment >= cutoff)
)

# Step 8.2: Manual local linear for Verbal Scores
verb_manual_win <- analysis_under80 %>%
  filter(abs(school_enrollment - cutoff) <= manual_bw) %>%
  filter(!is.na(avgverb), !is.na(school_enrollment), !is.na(above_cutoff))

verb_fit <- lm(avgverb ~ above_cutoff * enrollment_centered, data = verb_manual_win)
verb_coefs <- summary(verb_fit)$coefficients

verb_manual_res <- tibble::tibble(
  outcome = "avgverb",
  cutoff = cutoff,
  bandwidth = manual_bw,
  estimate = verb_coefs["above_cutoff", "Estimate"],
  std_error = verb_coefs["above_cutoff", "Std. Error"],
  p_value = verb_coefs["above_cutoff", "Pr(>|t|)"],
  n_left = sum(verb_manual_win$school_enrollment < cutoff),
  n_right = sum(verb_manual_win$school_enrollment >= cutoff)
)

# Step 8.3: Manual local linear for Class Size (First Stage Check)
class_manual_win <- analysis_under80 %>%
  filter(abs(school_enrollment - cutoff) <= manual_bw) %>%
  filter(!is.na(classize), !is.na(school_enrollment), !is.na(above_cutoff))

class_fit <- lm(classize ~ above_cutoff * enrollment_centered, data = class_manual_win)
class_coefs <- summary(class_fit)$coefficients

class_manual_res <- tibble::tibble(
  outcome = "classize",
  cutoff = cutoff,
  bandwidth = manual_bw,
  estimate = class_coefs["above_cutoff", "Estimate"],
  std_error = class_coefs["above_cutoff", "Std. Error"],
  p_value = class_coefs["above_cutoff", "Pr(>|t|)"],
  n_left = sum(class_manual_win$school_enrollment < cutoff),
  n_right = sum(class_manual_win$school_enrollment >= cutoff)
)

# Step 8.4: Manual local linear for Disadvantaged Share (Falsification check)
disadv_manual_win <- analysis_under80 %>%
  filter(abs(school_enrollment - cutoff) <= manual_bw) %>%
  filter(!is.na(disadvantaged), !is.na(school_enrollment), !is.na(above_cutoff))

disadv_fit <- lm(disadvantaged ~ above_cutoff * enrollment_centered, data = disadv_manual_win)
disadv_coefs <- summary(disadv_fit)$coefficients

disadv_manual_res <- tibble::tibble(
  outcome = "disadvantaged",
  cutoff = cutoff,
  bandwidth = manual_bw,
  estimate = disadv_coefs["above_cutoff", "Estimate"],
  std_error = disadv_coefs["above_cutoff", "Std. Error"],
  p_value = disadv_coefs["above_cutoff", "Pr(>|t|)"],
  n_left = sum(disadv_manual_win$school_enrollment < cutoff),
  n_right = sum(disadv_manual_win$school_enrollment >= cutoff)
)

# Combine manual results into a single table.
manual_results <- rbind(
  math_manual_res,
  verb_manual_res,
  class_manual_res,
  disadv_manual_res
)

# Save manual results to a professional HTML table file.
stargazer(
  as.data.frame(manual_results),
  type = "html",
  summary = FALSE,
  rownames = FALSE,
  title = "Table 4. Manual Local Linear RD Results (Bandwidth = 10)",
  digits = 3,
  out = "manual_local_linear_results.html"
)

# ==============================================================================
# SECTION 9: Part II, Question 8b - rdrobust Estimates (Default Settings)
# ==============================================================================

# Run rdrobust with default settings (which automatically chooses MSE-optimal bandwidth,
# local linear fits, and triangular kernel weights).

# Step 9.1: rdrobust for Math Scores
math_rd_ok <- !is.na(analysis_under80$school_enrollment) & !is.na(analysis_under80$avgmath)
math_rd_fit <- rdrobust(
  y = analysis_under80$avgmath[math_rd_ok],
  x = analysis_under80$school_enrollment[math_rd_ok],
  c = cutoff
)

math_rd_res <- tibble::tibble(
  outcome = "avgmath",
  cutoff = cutoff,
  estimate_conventional = unname(math_rd_fit$coef[1, 1]),
  se_conventional = unname(math_rd_fit$se[1, 1]),
  ci95_low_conventional = unname(math_rd_fit$ci[1, 1]),
  ci95_high_conventional = unname(math_rd_fit$ci[1, 2]),
  bandwidth_left = unname(math_rd_fit$bws[1, 1]),
  bandwidth_right = unname(math_rd_fit$bws[1, 2]),
  n_left = unname(math_rd_fit$N_h[1]),
  n_right = unname(math_rd_fit$N_h[2])
)

# Step 9.2: rdrobust for Verbal Scores
verb_rd_ok <- !is.na(analysis_under80$school_enrollment) & !is.na(analysis_under80$avgverb)
verb_rd_fit <- rdrobust(
  y = analysis_under80$avgverb[verb_rd_ok],
  x = analysis_under80$school_enrollment[verb_rd_ok],
  c = cutoff
)

verb_rd_res <- tibble::tibble(
  outcome = "avgverb",
  cutoff = cutoff,
  estimate_conventional = unname(verb_rd_fit$coef[1, 1]),
  se_conventional = unname(verb_rd_fit$se[1, 1]),
  ci95_low_conventional = unname(verb_rd_fit$ci[1, 1]),
  ci95_high_conventional = unname(verb_rd_fit$ci[1, 2]),
  bandwidth_left = unname(verb_rd_fit$bws[1, 1]),
  bandwidth_right = unname(verb_rd_fit$bws[1, 2]),
  n_left = unname(verb_rd_fit$N_h[1]),
  n_right = unname(verb_rd_fit$N_h[2])
)

# Combine rdrobust results into a single table.
rdrobust_results <- rbind(math_rd_res, verb_rd_res)

# Save rdrobust results to a professional HTML table file.
stargazer(
  as.data.frame(rdrobust_results),
  type = "html",
  summary = FALSE,
  rownames = FALSE,
  title = "Table 5. rdrobust Default RD Results",
  digits = 3,
  out = "rdrobust_default_results.html"
)

# ==============================================================================
# SECTION 10: Part II, Question 9 - Falsification Test
# ==============================================================================

# The disadvantaged manual local linear result (computed in Section 8) is exported
# as a standalone falsification check.
stargazer(
  as.data.frame(disadv_manual_res),
  type = "html",
  summary = FALSE,
  rownames = FALSE,
  title = "Table 6. Falsification Test: Discontinuity in Disadvantaged Share",
  digits = 3,
  out = "falsification_disadvantaged_results.html"
)

print("All quantitative regressions, plots, and tables have been generated successfully!")

# ==============================================================================
# Tyche SOP Output Disclosure
# ==============================================================================
# ---
# Generated for: Edgar Agunias
# Date: 2026-05-27
# Model: Gemini 3.5 Flash (Medium reasoning)
# Sources: Africa_GDP.Rda; grade5.dta; World Bank API indicators NY.GDP.PCAP.KD and SP.POP.TOTL
# Agent: Tyche
# ---
