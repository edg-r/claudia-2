################################################################################
# Homework 2 Integrated Script: Panel, TWFE, and RDD
################################################################################
# Setup
################################################################################

# Set the working folder so all input and output paths are relative to Homework 2.
setwd('/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Assignments/Homework 2')

# Add the local R package folder so the script can load rdrobust from this project.
.libPaths(c(normalizePath("outputs/part_ii/R_libs"), .libPaths()))

# Load packages for data cleaning, plotting, tables, Stata files, and RD estimation.
library(dplyr)
library(ggplot2)
library(jsonlite)
library(broom)
library(stargazer)
library(haven)
library(rdrobust)

# Define a helper that saves a data frame as a clean HTML table.
write_html_table <- function(df, file_name, title) {
  invisible(
    capture.output(
      stargazer(
        as.data.frame(df),
        type = "html",
        summary = FALSE,
        rownames = FALSE,
        title = title,
        digits = 3,
        out = file_name
      )
    )
  )
}

# Define a helper that saves one or more regression models as a clean HTML table.
write_model_table <- function(..., file_name) {
  invisible(
    capture.output(
      stargazer(
        ...,
        type = "html",
        omit.stat = c("f", "ser"),
        digits = 3,
        out = file_name
      )
    )
  )
}

################################################################################
# Part I: Panel and Two-Way Fixed Effects
################################################################################

# Load the professor-provided Africa panel data.
load("Africa_GDP.Rda")

# Stop immediately if the expected data object did not load.
stopifnot(exists("Africa_GDP"))

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

# Define a function that downloads one World Bank indicator for the analysis years.
fetch_wb_indicator <- function(indicator, years = analysis_years) {
  # Build the World Bank API URL for the selected indicator and year range.
  url <- paste0(
    "https://api.worldbank.org/v2/country/all/indicator/",
    indicator,
    "?format=json&date=",
    min(years),
    ":",
    max(years),
    "&per_page=20000"
  )

  # Read the JSON response from the World Bank API.
  raw <- jsonlite::fromJSON(url)

  # Stop if the API response is not in the expected data-frame format.
  if (length(raw) < 2 || !is.data.frame(raw[[2]])) {
    stop("World Bank API did not return a data frame for ", indicator)
  }

  # Keep the country name, country code, year, and numeric indicator value.
  raw[[2]] %>%
    transmute(
      wb_name = .data$country$value,
      iso3 = .data$countryiso3code,
      year = as.integer(.data$date),
      value = as.numeric(.data$value)
    )
}

# Download World Bank GDP per capita data.
gdp_pc_wb <- fetch_wb_indicator("NY.GDP.PCAP.KD") %>%
  rename(gdp_pc_constant_usd = value)

# Download World Bank population data.
pop_wb <- fetch_wb_indicator("SP.POP.TOTL") %>%
  rename(population = value)

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

# Save the Q1 regression table.
write_model_table(
  pooled_ols,
  within_lsdv,
  title = "GDP per Capita and Political Liberties, Average-Country Estimates",
  dep.var.labels = "GDP per capita (constant US dollars)",
  column.labels = c("Pooled OLS + year FE", "Country FE + year FE"),
  covariate.labels = "Political liberties",
  keep = "pol_lib",
  file_name = "table_q1_pooled_within.html"
)

################################################################################
# Q2: TWFE and Event Study Around Big Governance Improvements
################################################################################

# Run the TWFE model for the big governance improvement year.
twfe_bigimp <- lm(gdp_pc_constant_usd ~ bigimp + factor(country_id) + year_factor, data = complete_panel)

# Save the Q2 TWFE regression table.
write_model_table(
  twfe_bigimp,
  title = "TWFE Estimate for Large Governance Improvement Year",
  dep.var.labels = "GDP per capita (constant US dollars)",
  covariate.labels = "Big governance improvement year",
  keep = "bigimp",
  file_name = "table_q2_twfe_bigimp.html"
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

# Save the event-study coefficient table.
write_html_table(
  event_coef_plot_data,
  "event_study_leadlag_coefficients.html",
  "Event-Study Lead/Lag Coefficients"
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

# Save the residual event-study table.
write_html_table(
  event_summary,
  "event_study_residual_means.html",
  "Event-Study Residual Means"
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

# Save the Q4 population-weighted regression table.
write_model_table(
  weighted_pooled,
  weighted_within,
  title = "GDP per Capita and Political Liberties, Representative-Person Estimates",
  dep.var.labels = "GDP per capita (constant US dollars)",
  column.labels = c("Population-weighted pooled OLS + year FE", "Population-weighted country FE + year FE"),
  covariate.labels = "Political liberties",
  keep = "pol_lib",
  file_name = "table_q4_representative_person.html"
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

# Save the population-weighted event-study table.
write_html_table(
  weighted_event_summary,
  "weighted_event_study_residual_means.html",
  "Population-Weighted Event-Study Residual Means"
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

# Save the data schema table.
write_html_table(schema, "grade5_schema.html", "Grade 5 Data Schema")

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

# Open a PNG graphics device for the enrollment histogram.
png("hist_school_enrollment.png", width = 1600, height = 1000, res = 180)

# Plot the distribution of school enrollment and mark the cutoff.
print(
  ggplot(analysis, aes(x = school_enrollment)) +
    geom_histogram(binwidth = 5, boundary = 0, color = "white", fill = "#4C78A8") +
    geom_vline(xintercept = cutoff, color = "#C44E52", linewidth = 1) +
    labs(
      title = "Distribution of Fifth-Grade School Enrollment",
      subtitle = "Vertical line marks the Maimonides Rule cutoff at 40 students",
      x = "School enrollment",
      y = "Number of observations"
    ) +
    theme_minimal(base_size = 12)
)

# Close the PNG graphics device.
invisible(dev.off())

################################################################################
# Q7: Relationship Between Class Size and Scores
################################################################################

# Define a reusable function for RD-style outcome plots.
make_rdd_plot <- function(y_var, y_label, file_name) {
  # Keep schools below 80 students for the plot.
  plot_data <- subset(analysis, school_enrollment < max_enrollment)

  # Average the selected outcome at each enrollment value.
  bin_data <- aggregate(plot_data[[y_var]],
                        by = list(school_enrollment = plot_data$school_enrollment),
                        FUN = mean, na.rm = TRUE)

  # Rename the averaged outcome column.
  names(bin_data)[2] <- "mean_outcome"

  # Open a PNG graphics device for this outcome plot.
  png(file_name, width = 1600, height = 1000, res = 180)

  # Plot raw points, binned means, separate linear fits, and the cutoff.
  print(
    ggplot(plot_data, aes(x = school_enrollment, y = .data[[y_var]])) +
      geom_point(alpha = 0.18, color = "#4D4D4D", size = 1.1) +
      geom_point(data = bin_data, aes(y = mean_outcome), color = "#1B9E77", size = 2) +
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
        title = paste(y_label, "Around the Enrollment Cutoff"),
        subtitle = "Schools with enrollment below 80; separate linear fits on each side of 40",
        x = "School enrollment",
        y = y_label
      ) +
      theme_minimal(base_size = 12)
  )

  # Close the PNG graphics device.
  invisible(dev.off())
}

# Save the class-size RD plot.
make_rdd_plot("classize", "Class size", "rdd_classize_cutoff40.png")

# Save the math-score RD plot.
make_rdd_plot("avgmath", "Average math score", "rdd_avgmath_cutoff40.png")

# Save the verbal-score RD plot.
make_rdd_plot("avgverb", "Average verbal score", "rdd_avgverb_cutoff40.png")

################################################################################
# Q8a: Manual Local Linear RD
################################################################################

# Define a function that manually estimates a local linear RD effect.
manual_rd <- function(data, outcome, bw) {
  # Keep observations within the selected bandwidth around the cutoff.
  window <- subset(data, abs(school_enrollment - cutoff) <= bw)

  # Drop rows with missing outcome, enrollment, or cutoff-side indicator.
  window <- window[!is.na(window[[outcome]]) &
                     !is.na(window$school_enrollment) &
                     !is.na(window$above_cutoff), ]

  # Run a local linear model with separate slopes on each side of the cutoff.
  fit <- lm(reformulate(c("above_cutoff", "enrollment_centered",
                          "above_cutoff:enrollment_centered"), outcome), data = window)

  # Pull the coefficient table from the model summary.
  coefs <- summary(fit)$coefficients

  # Split the local sample into left and right sides of the cutoff.
  left <- subset(window, school_enrollment < cutoff)
  right <- subset(window, school_enrollment >= cutoff)

  # Return the cutoff estimate, standard error, p-value, and sample sizes.
  data.frame(
    outcome = outcome,
    cutoff = cutoff,
    bandwidth = bw,
    estimate = unname(coefs["above_cutoff", "Estimate"]),
    std_error = unname(coefs["above_cutoff", "Std. Error"]),
    p_value = unname(coefs["above_cutoff", "Pr(>|t|)"]),
    n_left = nrow(left),
    n_right = nrow(right),
    unique_schools_left = length(unique(left$schlcode)),
    unique_schools_right = length(unique(right$schlcode)),
    stringsAsFactors = FALSE
  )
}

# Estimate manual local linear RD effects for scores, class size, and disadvantage.
manual_results <- rbind(
  manual_rd(analysis_under80, "avgmath", manual_bw),
  manual_rd(analysis_under80, "avgverb", manual_bw),
  manual_rd(analysis_under80, "classize", manual_bw),
  manual_rd(analysis_under80, "disadvantaged", manual_bw)
)

# Save the manual local linear RD results table.
write_html_table(
  manual_results,
  "manual_local_linear_results.html",
  "Manual Local Linear RD Results"
)

################################################################################
# Q8b: rdrobust RD Estimates
################################################################################

# Define a function that estimates the RD effect using rdrobust.
rd_result <- function(outcome) {
  # Select the running variable and outcome.
  x <- analysis_under80$school_enrollment
  y <- analysis_under80[[outcome]]

  # Keep complete cases for the running variable and outcome.
  ok <- !is.na(x) & !is.na(y)

  # Run rdrobust at the cutoff.
  obj <- rdrobust(y = y[ok], x = x[ok], c = cutoff)

  # Store the confidence intervals, coefficients, and standard errors.
  ci <- obj$ci
  coef <- obj$coef
  se <- obj$se

  # Return the conventional estimate, standard error, CI, bandwidths, and sample sizes.
  data.frame(
    outcome = outcome,
    cutoff = cutoff,
    estimate_conventional = unname(coef[1, 1]),
    se_conventional = unname(se[1, 1]),
    ci95_low_conventional = unname(ci[1, 1]),
    ci95_high_conventional = unname(ci[1, 2]),
    bandwidth_left = unname(obj$bws[1, 1]),
    bandwidth_right = unname(obj$bws[1, 2]),
    n_left = unname(obj$N_h[1]),
    n_right = unname(obj$N_h[2]),
    stringsAsFactors = FALSE
  )
}

# Estimate rdrobust effects for math and verbal scores.
rdrobust_results <- rbind(rd_result("avgmath"), rd_result("avgverb"))

# Save the rdrobust results table.
write_html_table(
  rdrobust_results,
  "rdrobust_default_results.html",
  "rdrobust Default RD Results"
)
