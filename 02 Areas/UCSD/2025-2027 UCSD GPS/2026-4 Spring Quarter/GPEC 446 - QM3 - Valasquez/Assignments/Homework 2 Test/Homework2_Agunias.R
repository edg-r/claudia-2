################################################################################
# Homework 2 Integrated Script: Panel, TWFE, and RDD
################################################################################
# Setup
################################################################################

# Set the working folder so all input and output paths are relative to Homework 2.
#setwd('/Users/edgar/Documents/000 Files/02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez/Assignments/Homework 2 Test')

# Load packages for data cleaning, plotting, tables, Stata files, and RD estimation.
install.packages("rdrobust")
library(dplyr)
library(ggplot2)
library(jsonlite)
library(broom)
library(stargazer)
library(haven)
library(rdrobust)

################################################################################
# Part I: Panel and Two-Way Fixed Effects
################################################################################

# Load the professor-provided Africa panel data.
load("Africa_GDP.Rda")

# Store the assignment's analysis years.
analysis_years <- 1985:1998

# Create a lookup table that matches course-data country names to World Bank names.
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

################################################################################
# Part I Data: World Bank Join
################################################################################

# Build the World Bank API URL for GDP per capita.
gdp_pc_url <- paste0(
  "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.KD",
  "?format=json&date=",
  min(analysis_years),
  ":",
  max(analysis_years),
  "&per_page=20000"
)

# Read the GDP per capita JSON response.
gdp_pc_raw <- jsonlite::fromJSON(gdp_pc_url)

# Stop if the GDP per capita response is not in the expected format.
if (length(gdp_pc_raw) < 2 || !is.data.frame(gdp_pc_raw[[2]])) {
  stop("World Bank API did not return a data frame for GDP per capita")
}

# Keep country name, country code, year, and GDP per capita value.
gdp_pc_wb <- gdp_pc_raw[[2]] %>%
  transmute(
    wb_name = .data$country$value,
    iso3 = .data$countryiso3code,
    year = as.integer(.data$date),
    gdp_pc_constant_usd = as.numeric(.data$value)
  )

# Build the World Bank API URL for population.
pop_url <- paste0(
  "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL",
  "?format=json&date=",
  min(analysis_years),
  ":",
  max(analysis_years),
  "&per_page=20000"
)

# Read the population JSON response.
pop_raw <- jsonlite::fromJSON(pop_url)

# Stop if the population response is not in the expected format.
if (length(pop_raw) < 2 || !is.data.frame(pop_raw[[2]])) {
  stop("World Bank API did not return a data frame for population")
}

# Keep country name, country code, year, and population value.
pop_wb <- pop_raw[[2]] %>%
  transmute(
    wb_name = .data$country$value,
    iso3 = .data$countryiso3code,
    year = as.integer(.data$date),
    population = as.numeric(.data$value)
  )

# Build the main Part I analysis panel.
panel <- Africa_GDP %>%
  # Keep only the years required by the assignment.
  filter(year %in% analysis_years) %>%
  # Attach the World Bank country-name lookup.
  left_join(country_lookup, by = "country") %>%
  # Attach GDP per capita by country and year.
  left_join(gdp_pc_wb, by = c("wb_name", "year")) %>%
  # Attach population by country, year, and ISO code.
  left_join(pop_wb, by = c("wb_name", "year", "iso3")) %>%
  # Sort the panel by country and year.
  arrange(country, year) %>%
  # Create country IDs, year factors, and clean missing bigimp values.
  mutate(
    country_id = as.integer(factor(country, levels = sort(unique(country)))),
    year_factor = factor(year),
    bigimp = ifelse(is.na(bigimp), 0, bigimp)
  ) %>%
  # Work within each country to create event-study timing variables.
  group_by(country) %>%
  mutate(
    event_year = ifelse(any(bigimp == 1, na.rm = TRUE), year[which.max(bigimp)], NA_integer_),
    leadlag = ifelse(!is.na(event_year), year - event_year, NA_integer_)
  ) %>%
  ungroup()

# Create explicit year dummy variables for Question 1.
year_dummy_df <- model.matrix(~ factor(year) - 1, data = panel) %>%
  as.data.frame()

# Rename the year dummy columns to cleaner names.
names(year_dummy_df) <- sub("factor\\(year\\)", "year_", names(year_dummy_df))

# Attach the year dummy variables to the panel.
panel_with_dummies <- bind_cols(panel, year_dummy_df)

# Count country-years that are missing GDP or population after the World Bank join.
missing_join <- panel %>%
  filter(is.na(gdp_pc_constant_usd) | is.na(population)) %>%
  count(country, wb_name, iso3, name = "missing_rows")

# Store the total number of missing join rows for the summary file.
missing_join_rows <- sum(missing_join$missing_rows)

# Keep rows with both political liberties and GDP for the regression analysis.
complete_panel <- panel %>%
  filter(!is.na(pol_lib), !is.na(gdp_pc_constant_usd))

################################################################################
# Q1: Pooled OLS and Country Fixed Effects
################################################################################

# Run pooled OLS with year fixed effects.
pooled_ols <- lm(gdp_pc_constant_usd ~ pol_lib + year_factor, data = complete_panel)

# Run a country fixed-effects model with year fixed effects.
within_lsdv <- lm(gdp_pc_constant_usd ~ pol_lib + factor(country_id) + year_factor, data = complete_panel)

# Save the Q1 regression table with stargazer.
stargazer(
      pooled_ols,
      within_lsdv,
      type = "html",
      omit.stat = c("f", "ser"),
      digits = 3,
      title = "GDP per Capita and Political Liberties, Average-Country Estimates",
      dep.var.labels = "GDP per capita (constant US dollars)",
      column.labels = c("Pooled OLS + year FE", "Country FE + year FE"),
      covariate.labels = "Political liberties",
      keep = "pol_lib",
      out = "table_q1_pooled_within.html"
)

################################################################################
# Q2: TWFE and Event Study Around Big Governance Improvements
################################################################################

# Run the TWFE model for the big governance improvement year.
twfe_bigimp <- lm(gdp_pc_constant_usd ~ bigimp + factor(country_id) + year_factor, data = complete_panel)

# Save the Q2 TWFE regression table with stargazer.
stargazer(
      twfe_bigimp,
      type = "html",
      omit.stat = c("f", "ser"),
      digits = 3,
      title = "TWFE Estimate for Large Governance Improvement Year",
      dep.var.labels = "GDP per capita (constant US dollars)",
      covariate.labels = "Big governance improvement year",
      keep = "bigimp",
      out = "table_q2_twfe_bigimp.html"
)

# Keep event-study observations from five years before to five years after the event.
event_data <- complete_panel %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5) %>%
  # Convert event time to a factor and use year -1 as the reference period.
  mutate(leadlag_f = relevel(factor(leadlag), ref = "-1"))

# Estimate event-time coefficients with country and year fixed effects.
event_study_model <- lm(
  gdp_pc_constant_usd ~ leadlag_f + factor(country_id) + year_factor,
  data = event_data
)

# Extract only the event-time coefficients and confidence intervals.
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

# Add the omitted reference period back into the plot data as zero.
event_coef_plot_data <- bind_rows(
  event_coef_table,
  tibble::tibble(
    leadlag = -1,
    estimate = 0,
    std_error = 0,
    statistic = NA_real_,
    p_value = NA_real_,
    ci_low = 0,
    ci_high = 0
  )
) %>%
  arrange(leadlag)

# Save the event-study coefficient table with stargazer.
stargazer(
      as.data.frame(event_coef_plot_data),
      type = "html",
      summary = FALSE,
      rownames = FALSE,
      title = "Event-Study Lead/Lag Coefficients",
      digits = 3,
      out = "event_study_leadlag_coefficients.html"
)

# Create the Q2 event-study coefficient plot.
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
    y = "Change in GDP per capita relative to year -1"
  ) +
  theme_minimal(base_size = 12)

# Save the Q2 event-study coefficient plot.
ggsave("figure_q2_event_study_coefficients.png", event_plot, width = 8, height = 5, dpi = 300)
ggsave("figure_q2_event_study_residuals.png", event_plot, width = 8, height = 5, dpi = 300)

# Remove country and year fixed effects from GDP to create residuals.
twfe_resid_model <- lm(gdp_pc_constant_usd ~ factor(country_id) + year_factor, data = complete_panel)

# Attach the residuals and keep the event window.
residual_event_data <- complete_panel %>%
  mutate(twfe_residual = resid(twfe_resid_model)) %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5)

# Calculate average residual GDP by event year.
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

# Save the residual event-study table with stargazer.
stargazer(
      as.data.frame(event_summary),
      type = "html",
      summary = FALSE,
      rownames = FALSE,
      title = "Event-Study Residual Means",
      digits = 3,
      out = "event_study_residual_means.html"
)

# Create the residual event-study diagnostic plot.
residual_event_plot <- ggplot(event_summary, aes(x = leadlag, y = mean_residual)) +
  geom_hline(yintercept = 0, color = "gray45", linewidth = 0.4) +
  geom_vline(xintercept = 0, color = "firebrick", linewidth = 0.4, linetype = "dashed") +
  geom_errorbar(aes(ymin = ci_low, ymax = ci_high), width = 0.15, color = "gray35") +
  geom_line(color = "#1b4f72", linewidth = 0.7) +
  geom_point(color = "#1b4f72", size = 2) +
  scale_x_continuous(breaks = -5:5) +
  labs(
    title = "GDP per capita residuals around largest governance improvement",
    subtitle = "Residuals after removing country and year fixed effects",
    x = "Years relative to largest political-liberty improvement",
    y = "Mean GDP per capita residual (constant US dollars)"
  ) +
  theme_minimal(base_size = 12)

# Save the residual event-study diagnostic plot.
ggsave("figure_q2_event_study_residual_means_diagnostic.png", residual_event_plot, width = 8, height = 5, dpi = 300)

################################################################################
# Q4: Representative-Person Version
################################################################################

# Keep rows that have valid population weights.
representative_person <- complete_panel %>%
  filter(!is.na(population), population > 0)

# Run population-weighted pooled OLS.
weighted_pooled <- lm(
  gdp_pc_constant_usd ~ pol_lib + year_factor,
  data = representative_person,
  weights = population
)

# Run population-weighted country fixed effects.
weighted_within <- lm(
  gdp_pc_constant_usd ~ pol_lib + factor(country_id) + year_factor,
  data = representative_person,
  weights = population
)

# Save the Q4 population-weighted regression table with stargazer.
stargazer(
      weighted_pooled,
      weighted_within,
      type = "html",
      omit.stat = c("f", "ser"),
      digits = 3,
      title = "GDP per Capita and Political Liberties, Representative-Person Estimates",
      dep.var.labels = "GDP per capita (constant US dollars)",
      column.labels = c("Population-weighted pooled OLS + year FE", "Population-weighted country FE + year FE"),
      covariate.labels = "Political liberties",
      keep = "pol_lib",
      out = "table_q4_representative_person.html"
)

# Remove country and year fixed effects using population weights.
weighted_resid_model <- lm(
  gdp_pc_constant_usd ~ factor(country_id) + year_factor,
  data = representative_person,
  weights = population
)

# Attach weighted residuals and keep the event window.
weighted_event_data <- representative_person %>%
  mutate(weighted_twfe_residual = resid(weighted_resid_model)) %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5)

# Calculate population-weighted average residual GDP by event year.
weighted_event_summary <- weighted_event_data %>%
  group_by(leadlag) %>%
  summarise(
    weighted_mean_residual = weighted.mean(weighted_twfe_residual, w = population, na.rm = TRUE),
    total_population = sum(population, na.rm = TRUE),
    country_years = dplyr::n(),
    .groups = "drop"
  )

# Save the population-weighted event-study table with stargazer.
stargazer(
      as.data.frame(weighted_event_summary),
      type = "html",
      summary = FALSE,
      rownames = FALSE,
      title = "Population-Weighted Event-Study Residual Means",
      digits = 3,
      out = "weighted_event_study_residual_means.html"
)

# Create the population-weighted event-study plot.
weighted_event_plot <- ggplot(weighted_event_summary, aes(x = leadlag, y = weighted_mean_residual)) +
  geom_hline(yintercept = 0, color = "gray45", linewidth = 0.4) +
  geom_vline(xintercept = 0, color = "firebrick", linewidth = 0.4, linetype = "dashed") +
  geom_line(color = "#7d3c98", linewidth = 0.7) +
  geom_point(color = "#7d3c98", size = 2) +
  scale_x_continuous(breaks = -5:5) +
  labs(
    title = "Population-weighted GDP residuals around governance improvement",
    subtitle = "Representative-person version using World Bank population weights",
    x = "Years relative to largest political-liberty improvement",
    y = "Population-weighted mean GDP per capita residual"
  ) +
  theme_minimal(base_size = 12)

# Save the population-weighted event-study plot.
ggsave("figure_q4_weighted_event_study_residuals.png", weighted_event_plot, width = 8, height = 5, dpi = 300)

################################################################################
# Part II: Regression Discontinuity Design
################################################################################

# Store the Maimonides Rule cutoff.
cutoff <- 40

# Store the assignment's maximum enrollment restriction for RD estimates.
max_enrollment <- 80

# Store the manual bandwidth for local linear RD estimates.
manual_bw <- 10

################################################################################
# Part II Data
################################################################################

# Load the fifth-grade school data from the Stata file.
grade5 <- read_dta("grade5.dta")

# List the variables used in the RD analysis.
core_vars <- c("schlcode", "school_enrollment", "classize", "avgmath",
               "avgverb", "disadvantaged", "female", "religious")

# Create a data schema table with variable names, labels, missing values, and ranges.
schema <- data.frame(
  variable = names(grade5),
  class = vapply(grade5, function(x) paste(class(x), collapse = "/"), character(1)),
  label = vapply(grade5, function(x) {
    label <- attr(x, "label", exact = TRUE)
    if (is.null(label)) "" else as.character(label)
  }, character(1)),
  n_missing = vapply(grade5, function(x) sum(is.na(x)), integer(1)),
  min = vapply(grade5, function(x) if (is.numeric(x)) min(x, na.rm = TRUE) else NA_real_, numeric(1)),
  max = vapply(grade5, function(x) if (is.numeric(x)) max(x, na.rm = TRUE) else NA_real_, numeric(1))
)

# Save the data schema table with stargazer.
stargazer(
      as.data.frame(schema),
      type = "html",
      summary = FALSE,
      rownames = FALSE,
      title = "Grade 5 Data Schema",
      digits = 3,
      out = "grade5_schema.html"
)

# Keep only the core variables for the RD analysis.
analysis <- grade5[, core_vars]

# Center enrollment around the cutoff.
analysis$enrollment_centered <- analysis$school_enrollment - cutoff

# Create an indicator for being at or above the cutoff.
analysis$above_cutoff <- as.integer(analysis$school_enrollment >= cutoff)

# Keep the under-80 sample required for RD estimation.
analysis_under80 <- subset(analysis, school_enrollment < max_enrollment)

################################################################################
# Q6: Histogram of the Running Variable
################################################################################

# Create the enrollment histogram and mark the cutoff.
hist_school_enrollment_plot <- ggplot(analysis, aes(x = school_enrollment)) +
  geom_histogram(binwidth = 5, boundary = 0, color = "white", fill = "#4C78A8") +
  geom_vline(xintercept = cutoff, color = "#C44E52", linewidth = 1) +
  labs(
    title = "Distribution of Fifth-Grade School Enrollment",
    subtitle = "Vertical line marks the Maimonides Rule cutoff at 40 students",
    x = "School enrollment",
    y = "Number of observations"
  ) +
  theme_minimal(base_size = 12)

# Save the enrollment histogram with ggsave.
ggsave(
  "hist_school_enrollment.png",
  hist_school_enrollment_plot,
  width = 1600 / 180,
  height = 1000 / 180,
  dpi = 180
)

################################################################################
# Q7: Relationship Between Class Size and Scores
################################################################################

# Keep schools below 80 students for the Q7 plots.
plot_data <- subset(analysis, school_enrollment < max_enrollment)

# Average class size at each enrollment value.
classize_bin_data <- aggregate(
  plot_data$classize,
  by = list(school_enrollment = plot_data$school_enrollment),
  FUN = mean,
  na.rm = TRUE
)

# Rename the averaged class-size column.
names(classize_bin_data)[2] <- "mean_outcome"

# Create the class-size plot with separate linear fits on each side.
rdd_classize_plot <- ggplot(plot_data, aes(x = school_enrollment, y = classize)) +
  geom_point(alpha = 0.18, color = "#4D4D4D", size = 1.1) +
  geom_point(data = classize_bin_data, aes(y = mean_outcome), color = "#1B9E77", size = 2) +
  geom_smooth(
    data = subset(plot_data, school_enrollment < cutoff),
    method = "lm", formula = y ~ x, se = TRUE, color = "#1F77B4"
  ) +
  geom_smooth(
    data = subset(plot_data, school_enrollment >= cutoff),
    method = "lm", formula = y ~ x, se = TRUE, color = "#D62728"
  ) +
  geom_vline(xintercept = cutoff, color = "#C44E52", linewidth = 1) +
  labs(
    title = "Class size Around the Enrollment Cutoff",
    subtitle = "Schools with enrollment below 80; separate linear fits on each side of 40",
    x = "School enrollment",
    y = "Class size"
  ) +
  theme_minimal(base_size = 12)

# Save the class-size plot with ggsave.
ggsave(
  "rdd_classize_cutoff40.png",
  rdd_classize_plot,
  width = 1600 / 180,
  height = 1000 / 180,
  dpi = 180
)

# Average math scores at each enrollment value.
avgmath_bin_data <- aggregate(
  plot_data$avgmath,
  by = list(school_enrollment = plot_data$school_enrollment),
  FUN = mean,
  na.rm = TRUE
)

# Rename the averaged math-score column.
names(avgmath_bin_data)[2] <- "mean_outcome"

# Create the math-score plot with separate linear fits on each side.
rdd_avgmath_plot <- ggplot(plot_data, aes(x = school_enrollment, y = avgmath)) +
  geom_point(alpha = 0.18, color = "#4D4D4D", size = 1.1) +
  geom_point(data = avgmath_bin_data, aes(y = mean_outcome), color = "#1B9E77", size = 2) +
  geom_smooth(
    data = subset(plot_data, school_enrollment < cutoff),
    method = "lm", formula = y ~ x, se = TRUE, color = "#1F77B4"
  ) +
  geom_smooth(
    data = subset(plot_data, school_enrollment >= cutoff),
    method = "lm", formula = y ~ x, se = TRUE, color = "#D62728"
  ) +
  geom_vline(xintercept = cutoff, color = "#C44E52", linewidth = 1) +
  labs(
    title = "Average math score Around the Enrollment Cutoff",
    subtitle = "Schools with enrollment below 80; separate linear fits on each side of 40",
    x = "School enrollment",
    y = "Average math score"
  ) +
  theme_minimal(base_size = 12)

# Save the math-score plot with ggsave.
ggsave(
  "rdd_avgmath_cutoff40.png",
  rdd_avgmath_plot,
  width = 1600 / 180,
  height = 1000 / 180,
  dpi = 180
)

# Average verbal scores at each enrollment value.
avgverb_bin_data <- aggregate(
  plot_data$avgverb,
  by = list(school_enrollment = plot_data$school_enrollment),
  FUN = mean,
  na.rm = TRUE
)

# Rename the averaged verbal-score column.
names(avgverb_bin_data)[2] <- "mean_outcome"

# Create the verbal-score plot with separate linear fits on each side.
rdd_avgverb_plot <- ggplot(plot_data, aes(x = school_enrollment, y = avgverb)) +
  geom_point(alpha = 0.18, color = "#4D4D4D", size = 1.1) +
  geom_point(data = avgverb_bin_data, aes(y = mean_outcome), color = "#1B9E77", size = 2) +
  geom_smooth(
    data = subset(plot_data, school_enrollment < cutoff),
    method = "lm", formula = y ~ x, se = TRUE, color = "#1F77B4"
  ) +
  geom_smooth(
    data = subset(plot_data, school_enrollment >= cutoff),
    method = "lm", formula = y ~ x, se = TRUE, color = "#D62728"
  ) +
  geom_vline(xintercept = cutoff, color = "#C44E52", linewidth = 1) +
  labs(
    title = "Average verbal score Around the Enrollment Cutoff",
    subtitle = "Schools with enrollment below 80; separate linear fits on each side of 40",
    x = "School enrollment",
    y = "Average verbal score"
  ) +
  theme_minimal(base_size = 12)

# Save the verbal-score plot with ggsave.
ggsave(
  "rdd_avgverb_cutoff40.png",
  rdd_avgverb_plot,
  width = 1600 / 180,
  height = 1000 / 180,
  dpi = 180
)

################################################################################
# Q8a: Manual Local Linear RD
################################################################################

# Keep observations within 10 students of the cutoff for the math RD.
avgmath_window <- subset(analysis_under80, abs(school_enrollment - cutoff) <= manual_bw)

# Drop rows with missing math, enrollment, or cutoff-side indicator.
avgmath_window <- avgmath_window[!is.na(avgmath_window$avgmath) &
                                   !is.na(avgmath_window$school_enrollment) &
                                   !is.na(avgmath_window$above_cutoff), ]

# Estimate the manual local linear RD effect for math.
avgmath_fit <- lm(
  avgmath ~ above_cutoff + enrollment_centered + above_cutoff:enrollment_centered,
  data = avgmath_window
)

# Store the math model coefficient table.
avgmath_coefs <- summary(avgmath_fit)$coefficients

# Count math observations below and above the cutoff.
avgmath_left <- subset(avgmath_window, school_enrollment < cutoff)
avgmath_right <- subset(avgmath_window, school_enrollment >= cutoff)

# Save the math RD result as one table row.
avgmath_manual_result <- data.frame(
  outcome = "avgmath",
  cutoff = cutoff,
  bandwidth = manual_bw,
  estimate = unname(avgmath_coefs["above_cutoff", "Estimate"]),
  std_error = unname(avgmath_coefs["above_cutoff", "Std. Error"]),
  p_value = unname(avgmath_coefs["above_cutoff", "Pr(>|t|)"]),
  n_left = nrow(avgmath_left),
  n_right = nrow(avgmath_right),
  unique_schools_left = length(unique(avgmath_left$schlcode)),
  unique_schools_right = length(unique(avgmath_right$schlcode)),
  stringsAsFactors = FALSE
)

# Keep observations within 10 students of the cutoff for the verbal RD.
avgverb_window <- subset(analysis_under80, abs(school_enrollment - cutoff) <= manual_bw)

# Drop rows with missing verbal score, enrollment, or cutoff-side indicator.
avgverb_window <- avgverb_window[!is.na(avgverb_window$avgverb) &
                                   !is.na(avgverb_window$school_enrollment) &
                                   !is.na(avgverb_window$above_cutoff), ]

# Estimate the manual local linear RD effect for verbal scores.
avgverb_fit <- lm(
  avgverb ~ above_cutoff + enrollment_centered + above_cutoff:enrollment_centered,
  data = avgverb_window
)

# Store the verbal model coefficient table.
avgverb_coefs <- summary(avgverb_fit)$coefficients

# Count verbal observations below and above the cutoff.
avgverb_left <- subset(avgverb_window, school_enrollment < cutoff)
avgverb_right <- subset(avgverb_window, school_enrollment >= cutoff)

# Save the verbal RD result as one table row.
avgverb_manual_result <- data.frame(
  outcome = "avgverb",
  cutoff = cutoff,
  bandwidth = manual_bw,
  estimate = unname(avgverb_coefs["above_cutoff", "Estimate"]),
  std_error = unname(avgverb_coefs["above_cutoff", "Std. Error"]),
  p_value = unname(avgverb_coefs["above_cutoff", "Pr(>|t|)"]),
  n_left = nrow(avgverb_left),
  n_right = nrow(avgverb_right),
  unique_schools_left = length(unique(avgverb_left$schlcode)),
  unique_schools_right = length(unique(avgverb_right$schlcode)),
  stringsAsFactors = FALSE
)

# Keep observations within 10 students of the cutoff for the class-size RD.
classize_window <- subset(analysis_under80, abs(school_enrollment - cutoff) <= manual_bw)

# Drop rows with missing class size, enrollment, or cutoff-side indicator.
classize_window <- classize_window[!is.na(classize_window$classize) &
                                     !is.na(classize_window$school_enrollment) &
                                     !is.na(classize_window$above_cutoff), ]

# Estimate the manual local linear RD effect for class size.
classize_fit <- lm(
  classize ~ above_cutoff + enrollment_centered + above_cutoff:enrollment_centered,
  data = classize_window
)

# Store the class-size model coefficient table.
classize_coefs <- summary(classize_fit)$coefficients

# Count class-size observations below and above the cutoff.
classize_left <- subset(classize_window, school_enrollment < cutoff)
classize_right <- subset(classize_window, school_enrollment >= cutoff)

# Save the class-size RD result as one table row.
classize_manual_result <- data.frame(
  outcome = "classize",
  cutoff = cutoff,
  bandwidth = manual_bw,
  estimate = unname(classize_coefs["above_cutoff", "Estimate"]),
  std_error = unname(classize_coefs["above_cutoff", "Std. Error"]),
  p_value = unname(classize_coefs["above_cutoff", "Pr(>|t|)"]),
  n_left = nrow(classize_left),
  n_right = nrow(classize_right),
  unique_schools_left = length(unique(classize_left$schlcode)),
  unique_schools_right = length(unique(classize_right$schlcode)),
  stringsAsFactors = FALSE
)

# Keep observations within 10 students of the cutoff for the disadvantage falsification test.
disadvantaged_window <- subset(analysis_under80, abs(school_enrollment - cutoff) <= manual_bw)

# Drop rows with missing disadvantage, enrollment, or cutoff-side indicator.
disadvantaged_window <- disadvantaged_window[!is.na(disadvantaged_window$disadvantaged) &
                                               !is.na(disadvantaged_window$school_enrollment) &
                                               !is.na(disadvantaged_window$above_cutoff), ]

# Estimate the manual local linear RD effect for disadvantage.
disadvantaged_fit <- lm(
  disadvantaged ~ above_cutoff + enrollment_centered + above_cutoff:enrollment_centered,
  data = disadvantaged_window
)

# Store the disadvantage model coefficient table.
disadvantaged_coefs <- summary(disadvantaged_fit)$coefficients

# Count disadvantage observations below and above the cutoff.
disadvantaged_left <- subset(disadvantaged_window, school_enrollment < cutoff)
disadvantaged_right <- subset(disadvantaged_window, school_enrollment >= cutoff)

# Save the disadvantage RD result as one table row.
disadvantaged_manual_result <- data.frame(
  outcome = "disadvantaged",
  cutoff = cutoff,
  bandwidth = manual_bw,
  estimate = unname(disadvantaged_coefs["above_cutoff", "Estimate"]),
  std_error = unname(disadvantaged_coefs["above_cutoff", "Std. Error"]),
  p_value = unname(disadvantaged_coefs["above_cutoff", "Pr(>|t|)"]),
  n_left = nrow(disadvantaged_left),
  n_right = nrow(disadvantaged_right),
  unique_schools_left = length(unique(disadvantaged_left$schlcode)),
  unique_schools_right = length(unique(disadvantaged_right$schlcode)),
  stringsAsFactors = FALSE
)

# Combine the four manual RD result rows into one table.
manual_results <- rbind(
  avgmath_manual_result,
  avgverb_manual_result,
  classize_manual_result,
  disadvantaged_manual_result
)

# Save the manual local linear RD results table with stargazer.
stargazer(
      as.data.frame(manual_results),
      type = "html",
      summary = FALSE,
      rownames = FALSE,
      title = "Manual Local Linear RD Results",
      digits = 3,
      out = "manual_local_linear_results.html"
)

################################################################################
# Q8b: rdrobust RD Estimates
################################################################################

# Select the running variable and math outcome for rdrobust.
rd_avgmath_x <- analysis_under80$school_enrollment
rd_avgmath_y <- analysis_under80$avgmath

# Keep complete cases for the math rdrobust estimate.
rd_avgmath_ok <- !is.na(rd_avgmath_x) & !is.na(rd_avgmath_y)

# Run rdrobust for math scores at the cutoff.
rd_avgmath_obj <- rdrobust(y = rd_avgmath_y[rd_avgmath_ok], x = rd_avgmath_x[rd_avgmath_ok], c = cutoff)

# Store the math rdrobust confidence intervals, coefficients, and standard errors.
rd_avgmath_ci <- rd_avgmath_obj$ci
rd_avgmath_coef <- rd_avgmath_obj$coef
rd_avgmath_se <- rd_avgmath_obj$se

# Save the math rdrobust result as one table row.
rd_avgmath_result <- data.frame(
  outcome = "avgmath",
  cutoff = cutoff,
  estimate_conventional = unname(rd_avgmath_coef[1, 1]),
  se_conventional = unname(rd_avgmath_se[1, 1]),
  ci95_low_conventional = unname(rd_avgmath_ci[1, 1]),
  ci95_high_conventional = unname(rd_avgmath_ci[1, 2]),
  bandwidth_left = unname(rd_avgmath_obj$bws[1, 1]),
  bandwidth_right = unname(rd_avgmath_obj$bws[1, 2]),
  n_left = unname(rd_avgmath_obj$N_h[1]),
  n_right = unname(rd_avgmath_obj$N_h[2]),
  stringsAsFactors = FALSE
)

# Select the running variable and verbal outcome for rdrobust.
rd_avgverb_x <- analysis_under80$school_enrollment
rd_avgverb_y <- analysis_under80$avgverb

# Keep complete cases for the verbal rdrobust estimate.
rd_avgverb_ok <- !is.na(rd_avgverb_x) & !is.na(rd_avgverb_y)

# Run rdrobust for verbal scores at the cutoff.
rd_avgverb_obj <- rdrobust(y = rd_avgverb_y[rd_avgverb_ok], x = rd_avgverb_x[rd_avgverb_ok], c = cutoff)

# Store the verbal rdrobust confidence intervals, coefficients, and standard errors.
rd_avgverb_ci <- rd_avgverb_obj$ci
rd_avgverb_coef <- rd_avgverb_obj$coef
rd_avgverb_se <- rd_avgverb_obj$se

# Save the verbal rdrobust result as one table row.
rd_avgverb_result <- data.frame(
  outcome = "avgverb",
  cutoff = cutoff,
  estimate_conventional = unname(rd_avgverb_coef[1, 1]),
  se_conventional = unname(rd_avgverb_se[1, 1]),
  ci95_low_conventional = unname(rd_avgverb_ci[1, 1]),
  ci95_high_conventional = unname(rd_avgverb_ci[1, 2]),
  bandwidth_left = unname(rd_avgverb_obj$bws[1, 1]),
  bandwidth_right = unname(rd_avgverb_obj$bws[1, 2]),
  n_left = unname(rd_avgverb_obj$N_h[1]),
  n_right = unname(rd_avgverb_obj$N_h[2]),
  stringsAsFactors = FALSE
)

# Combine the math and verbal rdrobust result rows into one table.
rdrobust_results <- rbind(rd_avgmath_result, rd_avgverb_result)

# Save the rdrobust results table with stargazer.
stargazer(
      as.data.frame(rdrobust_results),
      type = "html",
      summary = FALSE,
      rownames = FALSE,
      title = "rdrobust Default RD Results",
      digits = 3,
      out = "rdrobust_default_results.html"
)