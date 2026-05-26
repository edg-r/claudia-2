################################################################################
# Homework 2 Part I: Panel and Two-Way Fixed Effects
################################################################################

# This script answers Questions 1-4. The goal is to connect the supplied
# governance panel to World Bank income/population data, then compare the
# average-country results with the representative-person results.

################################################################################
# Setup & Output Folders
################################################################################

setwd('/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Assignments/Homework 2')

library(dplyr)
library(ggplot2)
library(jsonlite)
library(broom)
library(stargazer)
library(fixest)

#write table code for standardized stargazer output and easier calling
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
        out = file.path(out_dir, file_name)
      )
    )
  )
}

write_model_table <- function(..., file_name) {
  invisible(
    capture.output(
      stargazer(
        ...,
        type = "html",
        omit.stat = c("f", "ser"),
        digits = 3,
        out = file.path(out_dir, file_name)
      )
    )
  )
}

################################################################################
# Load Governance Panel
################################################################################

# The professor-provided file stores political liberties and the big-improvement
# marker. The analysis window follows the assignment prompt: 1985-1998.
load(file.path(base_dir, "Africa_GDP.Rda"))
stopifnot(exists("Africa_GDP"))

analysis_years <- 1985:1998

# Match the country names in the class file to the World Bank API names.
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
# Fetch World Bank GDP and Population Data
################################################################################

# Pull World Bank indicators directly so the homework can be regenerated later.
# GDP per capita is the income outcome; population is needed for Question 4.
fetch_wb_indicator <- function(indicator, years = analysis_years) {
  url <- paste0(
    "https://api.worldbank.org/v2/country/all/indicator/",
    indicator,
    "?format=json&date=",
    min(years),
    ":",
    max(years),
    "&per_page=20000"
  )
  raw <- jsonlite::fromJSON(url)
  if (length(raw) < 2 || !is.data.frame(raw[[2]])) {
    stop("World Bank API did not return a data frame for ", indicator)
  }
  raw[[2]] %>%
    transmute(
      wb_name = .data$country$value,
      iso3 = .data$countryiso3code,
      year = as.integer(.data$date),
      value = as.numeric(.data$value)
    )
}

gdp_pc_wb <- fetch_wb_indicator("NY.GDP.PCAP.KD") %>%
  rename(gdp_pc_constant_usd = value)

pop_wb <- fetch_wb_indicator("SP.POP.TOTL") %>%
  rename(population = value)

################################################################################
# Build Analysis Panel
################################################################################

# Join governance, GDP, and population. Then add the numeric country identifier,
# year dummies, and event-time variable needed for the event-study graph.
panel <- Africa_GDP %>%
  filter(year %in% analysis_years) %>%
  left_join(country_lookup, by = "country") %>%
  left_join(gdp_pc_wb, by = c("wb_name", "year")) %>%
  left_join(pop_wb, by = c("wb_name", "year", "iso3")) %>%
  arrange(country, year) %>%
  mutate(
    country_id = as.integer(factor(country, levels = sort(unique(country)))),
    year_factor = factor(year),
    bigimp = ifelse(is.na(bigimp), 0, bigimp)
  ) %>%
  group_by(country) %>%
  mutate(
    event_year = ifelse(any(bigimp == 1, na.rm = TRUE), year[which.max(bigimp)], NA_integer_),
    leadlag = ifelse(!is.na(event_year), year - event_year, NA_integer_)
  ) %>%
  ungroup()

year_dummy_df <- model.matrix(~ factor(year) - 1, data = panel) %>%
  as.data.frame()
names(year_dummy_df) <- sub("factor\\(year\\)", "year_", names(year_dummy_df))
panel_with_dummies <- bind_cols(panel, year_dummy_df)

# Keep a small audit trail for unmatched World Bank rows.
missing_join <- panel %>%
  filter(is.na(gdp_pc_constant_usd) | is.na(population)) %>%
  count(country, wb_name, iso3, name = "missing_rows")
missing_join_rows <- sum(missing_join$missing_rows)

complete_panel <- panel %>%
  filter(!is.na(pol_lib), !is.na(gdp_pc_constant_usd))

################################################################################
# Q1: Pooled OLS and Country Fixed Effects
################################################################################

# Pooled OLS compares richer and poorer country-years. The within/LSDV model
# compares a country to itself after absorbing country and year fixed effects.
pooled_ols <- lm(gdp_pc_constant_usd ~ pol_lib + year_factor, data = complete_panel)
within_lsdv <- lm(gdp_pc_constant_usd ~ pol_lib + factor(country_id) + year_factor, data = complete_panel)

# Pull the coefficient rows needed for the notes file.
extract_key <- function(model, model_name, terms = c("pol_lib", "bigimp")) {
  n_val <- length(model$residuals)
  model_summary <- summary(model)
  broom::tidy(model) %>%
    filter(term %in% terms) %>%
    transmute(
      model = model_name,
      term,
      estimate,
      std_error = std.error,
      statistic,
      p_value = p.value,
      n = n_val,
      r_squared = model_summary$r.squared,
      adj_r_squared = model_summary$adj.r.squared
    )
}

table_q1 <- bind_rows(
  extract_key(pooled_ols, "Pooled OLS + year FE", "pol_lib"),
  extract_key(within_lsdv, "Within/LSDV: country FE + year FE", "pol_lib")
)
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

# The TWFE coefficient checks whether GDP is different in the exact year marked
# as the largest political-liberty improvement, after country and year fixed effects.
twfe_bigimp <- feols(gdp_pc_constant_usd ~ bigimp | country + year, data = complete_panel)

table_twfe <- extract_key(twfe_bigimp, "TWFE big improvement indicator", "bigimp")
write_model_table(
  twfe_bigimp,
  title = "TWFE Estimate for Large Governance Improvement Year",
  dep.var.labels = "GDP per capita (constant US dollars)",
  covariate.labels = "Big governance improvement year",
  keep = "bigimp",
  file_name = "table_q2_twfe_bigimp.html"
)

# Build the event-study structure the same way as Lab 5: restrict to the
# analysis window around treatment, make event time a factor, omit tau = -1 as
# the reference period, and estimate one coefficient for each event-time period.
event_data <- complete_panel %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5) %>%
  mutate(leadlag_f = relevel(factor(leadlag), ref = "-1"))

event_study_model <- lm(
  gdp_pc_constant_usd ~ leadlag_f + factor(country_id) + year_factor,
  data = event_data
)

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

# Add the omitted reference period, just like Lab 5 adds tau = -1 back to the
# coefficient data before plotting.
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
write_html_table(
  event_coef_plot_data,
  "event_study_leadlag_coefficients.html",
  "Event-Study Lead/Lag Coefficients"
)

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
ggsave(file.path(out_dir, "figure_q2_event_study_coefficients.png"), event_plot, width = 8, height = 5, dpi = 300)
ggsave(file.path(out_dir, "figure_q2_event_study_residuals.png"), event_plot, width = 8, height = 5, dpi = 300)

# Keep the older residual-means summary as a diagnostic output. The submitted Q2
# figure above now follows the Lab 5 coefficient-event-study template.
twfe_resid_model <- lm(gdp_pc_constant_usd ~ factor(country_id) + year_factor, data = complete_panel)
residual_event_data <- complete_panel %>%
  mutate(twfe_residual = resid(twfe_resid_model)) %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5)

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
write_html_table(
  event_summary,
  "event_study_residual_means.html",
  "Event-Study Residual Means"
)

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
ggsave(
  file.path(out_dir, "figure_q2_event_study_residual_means_diagnostic.png"),
  residual_event_plot,
  width = 8,
  height = 5,
  dpi = 300
)

################################################################################
# Q4: Representative-Person Version
################################################################################

# Weight by population so large countries count more. This changes the estimand
# from the average African country-year to the average African person-year.
representative_person <- complete_panel %>%
  filter(!is.na(population), population > 0)

weighted_pooled <- lm(
  gdp_pc_constant_usd ~ pol_lib + year_factor,
  data = representative_person,
  weights = population
)
weighted_within <- lm(
  gdp_pc_constant_usd ~ pol_lib + factor(country_id) + year_factor,
  data = representative_person,
  weights = population
)

table_q4 <- bind_rows(
  extract_key(weighted_pooled, "Population-weighted pooled OLS + year FE", "pol_lib"),
  extract_key(weighted_within, "Population-weighted country FE + year FE", "pol_lib")
)
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

weighted_resid_model <- lm(
  gdp_pc_constant_usd ~ factor(country_id) + year_factor,
  data = representative_person,
  weights = population
)
weighted_event_data <- representative_person %>%
  mutate(weighted_twfe_residual = resid(weighted_resid_model)) %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5)

weighted_event_summary <- weighted_event_data %>%
  group_by(leadlag) %>%
  summarise(
    weighted_mean_residual = weighted.mean(weighted_twfe_residual, w = population, na.rm = TRUE),
    total_population = sum(population, na.rm = TRUE),
    country_years = dplyr::n(),
    .groups = "drop"
  )
write_html_table(
  weighted_event_summary,
  "weighted_event_study_residual_means.html",
  "Population-Weighted Event-Study Residual Means"
)

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
ggsave(file.path(out_dir, "figure_q4_weighted_event_study_residuals.png"), weighted_event_plot, width = 8, height = 5, dpi = 300)

################################################################################
# Write Part I Notes
################################################################################

# Build a short Markdown note file from the model output. The final report uses
# this file as the interpretation source for Questions 1-4.
make_md_table <- function(df, digits = 3) {
  df_print <- df %>%
    mutate(across(where(is.numeric), ~ round(.x, digits)))
  paste(capture.output(knitr::kable(df_print, format = "pipe")), collapse = "\n")
}

interpretation <- c(
  "# Homework 2 Part I Notes",
  "",
  "## Data",
  paste0("- Governance panel: `Africa_GDP.Rda`, filtered to ", min(analysis_years), "-", max(analysis_years), "."),
  "- GDP per capita: World Bank indicator `NY.GDP.PCAP.KD` (constant US dollars).",
  "- Population: World Bank indicator `SP.POP.TOTL`, used as weights for the representative-person version.",
  paste0("- Final country-year rows with GDP and governance: ", nrow(complete_panel), "."),
  paste0("- Country-year rows missing GDP or population after World Bank join: ", missing_join_rows, "."),
  "",
  "## Q1 Table: average-country estimates",
  make_md_table(table_q1),
  "",
  "Interpretation: the pooled model compares richer and poorer country-years after absorbing common year shocks; the within model asks whether a given country is richer in years when its political-liberty score is higher, net of country and year fixed effects.",
  "",
  "## Q2 TWFE big-improvement estimate",
  make_md_table(table_twfe),
  "",
  "The event-study figure follows the Lab 5 template: construct event time around the treatment year, omit year -1 as the reference period, estimate one TWFE coefficient for each lead/lag, and plot coefficients with 95% confidence intervals. Points before zero are pre-improvement years; points after zero are post-improvement years. A clear upward pre-trend would suggest income growth precedes governance improvement; post-zero movement would be more consistent with income changes following the governance event.",
  "",
  "## Q4 Table: representative-person estimates",
  make_md_table(table_q4),
  "",
  "Population weighting changes the estimand from the average country-year to the average person-year. Large-population countries, especially Nigeria, Ethiopia, Democratic Republic of Congo, South Africa, Tanzania, Kenya, Sudan, and Uganda, therefore receive much more influence than small countries such as Seychelles, Sao Tome and Principe, and Comoros.",
  "",
  "## Files generated",
  "- `table_q1_pooled_within.html`",
  "- `table_q2_twfe_bigimp.html`",
  "- `event_study_residual_means.html`",
  "- `event_study_leadlag_coefficients.html`",
  "- `figure_q2_event_study_coefficients.png`",
  "- `figure_q2_event_study_residuals.png`",
  "- `figure_q2_event_study_residual_means_diagnostic.png`",
  "- `table_q4_representative_person.html`",
  "- `weighted_event_study_residual_means.html`",
  "- `figure_q4_weighted_event_study_residuals.png`",
  "",
  "---",
  "Generated for: Edgar Agunias",
  paste0("Date: ", Sys.Date()),
  "Model: GPT-5 Codex",
  "Sources: Africa_GDP.Rda; Homework 2 Panel & RDD prompt; World Bank API indicators NY.GDP.PCAP.KD and SP.POP.TOTL",
  "Agent: Tyche",
  "---"
)
writeLines(interpretation, file.path(base_dir, "PART_I_NOTES.md"))

cat("Part I complete. Outputs written to:", out_dir, "\n")
