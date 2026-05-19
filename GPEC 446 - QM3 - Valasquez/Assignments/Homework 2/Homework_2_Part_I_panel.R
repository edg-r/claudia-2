################################################################################
# Homework 2 Part I: Panel and Two-Way Fixed Effects
################################################################################

# This script answers Questions 1-4. The goal is to connect the supplied
# governance panel to World Bank income/population data, then compare the
# average-country results with the representative-person results.

################################################################################
# Setup & Output Folders
################################################################################

required <- c("dplyr", "ggplot2", "jsonlite", "readr", "broom")
missing_pkgs <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing_pkgs) > 0) {
  stop("Missing required R packages: ", paste(missing_pkgs, collapse = ", "))
}

library(dplyr)
library(ggplot2)
library(jsonlite)
library(readr)
library(broom)

# Locate the folder that contains the homework files. This lets the script run
# either from RStudio or from the terminal with `Rscript Homework_2_Part_I_panel.R`.
script_arg <- grep("^--file=", commandArgs(FALSE), value = TRUE)
script_path <- if (length(script_arg) > 0) sub("^--file=", "", script_arg[[1]]) else "Homework_2_Part_I_panel.R"
base_dir <- dirname(normalizePath(script_path, mustWork = FALSE))
if (!file.exists(file.path(base_dir, "Africa_GDP.Rda"))) {
  base_dir <- "/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Assignments/Homework 2"
}
out_dir <- file.path(base_dir, "outputs", "part_i")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

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

# Save the joined panel so the data-cleaning step is visible and checkable.
write_csv(panel_with_dummies, file.path(out_dir, "part_i_analysis_panel.csv"))

# Keep a small audit trail for unmatched World Bank rows.
missing_join <- panel %>%
  filter(is.na(gdp_pc_constant_usd) | is.na(population)) %>%
  count(country, wb_name, iso3, name = "missing_rows")
write_csv(missing_join, file.path(out_dir, "part_i_missing_wb_join_rows.csv"))
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

# Pull the coefficient rows needed for clean CSV tables.
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
write_csv(table_q1, file.path(out_dir, "table_q1_pooled_within.csv"))

################################################################################
# Q2: TWFE and Event Study Around Big Governance Improvements
################################################################################

# The TWFE coefficient checks whether GDP is different in the exact year marked
# as the largest political-liberty improvement, after country and year fixed effects.
twfe_bigimp <- lm(gdp_pc_constant_usd ~ bigimp + factor(country_id) + year_factor, data = complete_panel)

table_twfe <- extract_key(twfe_bigimp, "TWFE big improvement indicator", "bigimp")
write_csv(table_twfe, file.path(out_dir, "table_q2_twfe_bigimp.csv"))

# Remove country and year fixed effects, then graph average residual GDP around
# each country's largest governance improvement.
twfe_resid_model <- lm(gdp_pc_constant_usd ~ factor(country_id) + year_factor, data = complete_panel)
event_data <- complete_panel %>%
  mutate(twfe_residual = resid(twfe_resid_model)) %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5)

event_summary <- event_data %>%
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
write_csv(event_summary, file.path(out_dir, "event_study_residual_means.csv"))

event_coef <- lm(twfe_residual ~ relevel(factor(leadlag), ref = "-1"), data = event_data)
event_coef_table <- broom::tidy(event_coef) %>%
  filter(term != "(Intercept)") %>%
  mutate(leadlag = as.integer(gsub("relevel\\(factor\\(leadlag\\), ref = \"-1\"\\)", "", term)))
write_csv(event_coef_table, file.path(out_dir, "event_study_leadlag_coefficients.csv"))

event_plot <- ggplot(event_summary, aes(x = leadlag, y = mean_residual)) +
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
ggsave(file.path(out_dir, "figure_q2_event_study_residuals.png"), event_plot, width = 8, height = 5, dpi = 300)

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
write_csv(table_q4, file.path(out_dir, "table_q4_representative_person.csv"))

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
write_csv(weighted_event_summary, file.path(out_dir, "weighted_event_study_residual_means.csv"))

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
  "The event-study figure should be read as residual GDP per capita after country and year fixed effects. Points before zero are pre-improvement years; points after zero are post-improvement years. A clear upward slope before zero would suggest income growth precedes governance improvement; movement after zero would be more consistent with income changes following the governance event.",
  "",
  "## Q4 Table: representative-person estimates",
  make_md_table(table_q4),
  "",
  "Population weighting changes the estimand from the average country-year to the average person-year. Large-population countries, especially Nigeria, Ethiopia, Democratic Republic of Congo, South Africa, Tanzania, Kenya, Sudan, and Uganda, therefore receive much more influence than small countries such as Seychelles, Sao Tome and Principe, and Comoros.",
  "",
  "## Files generated",
  "- `part_i_analysis_panel.csv`",
  "- `part_i_missing_wb_join_rows.csv`",
  "- `table_q1_pooled_within.csv`",
  "- `table_q2_twfe_bigimp.csv`",
  "- `event_study_residual_means.csv`",
  "- `event_study_leadlag_coefficients.csv`",
  "- `figure_q2_event_study_residuals.png`",
  "- `table_q4_representative_person.csv`",
  "- `weighted_event_study_residual_means.csv`",
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
