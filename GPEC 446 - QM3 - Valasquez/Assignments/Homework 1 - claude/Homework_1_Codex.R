################################################################################
# Setup
#
# Assignment role:
# This is not one of the numbered homework questions. It loads the packages,
# sets knitting options, and defines helper functions used throughout the file.
################################################################################

## ----setup, include=FALSE-----------------------------------------------------
# Set global knitting options once so tables/figures print consistently.
knitr::opts_chunk$set(
  echo = TRUE,
  warning = FALSE,
  message = FALSE,
  fig.width = 9,
  fig.height = 6
)

library(dplyr)
library(ggplot2)
library(readr)
library(broom)
library(knitr)
library(kableExtra)
library(stargazer)
library(AER)

# Define small formatting helpers up front so every table uses the same style.
fmt_num <- function(x, digits = 2) formatC(x, format = "f", digits = digits, big.mark = ",")
fmt_coef <- function(est, se, digits = 3) sprintf("%s (%s)", fmt_num(est, digits), fmt_num(se, digits))


################################################################################
# Opportunity Atlas: Shared Data Preparation
#
# Assignment role:
# This supports the Opportunity Atlas questions. It loads atlas.csv and creates
# variables that are used repeatedly in the descriptive statistics and regression
# analysis sections.
################################################################################

## ----data---------------------------------------------------------------------
# Load the main tract-level dataset and construct the variables used across questions.
atlas <- read_csv("atlas.csv", show_col_types = FALSE) %>%
  mutate(
    # Regression questions 4-5: create the required majority-non-white dummy.
    majority_non_white = if_else(share_white2000 < 0.5, 1, 0, missing = NA_integer_),
    # Regression questions 3-9: put poverty on a percentage-point scale.
    poverty_pp = poor_share1990 * 100,
    # Regression tables: express child income in thousands of dollars.
    mobility_k = kfr_pooled_p25 / 1000,
    # Descriptive statistics question 2: build the tract FIPS code used on the map.
    tract_code = sprintf("%06d", as.integer(round(tract))),
    fips = sprintf("%02d%03d%s", as.integer(state), as.integer(county), tract_code)
  )


################################################################################
# Question 1: Descriptive Statistics
#
# Choose one city from Los Angeles, New York, Chicago, or New Orleans. Describe
# clustering and variation in average income levels on the Opportunity Atlas map.
################################################################################

# Isolate the four cities used in the comparative scatterplot exercise.
cities <- c("Los Angeles", "New York", "Chicago", "New Orleans")
city_data <- atlas %>% filter(czname %in% cities)

# Focus the tract-level descriptive work on the city chosen for the homework narrative.
chosen_city <- "New Orleans"
chosen_city_data <- atlas %>% filter(czname == chosen_city)

# Print a quick on-screen summary of the chosen city so Q1 stands on its own.
cat("\n==================== Question 1 ====================\n")
cat("Chosen city:", chosen_city, "\n")
cat("Number of tracts in chosen city:", nrow(chosen_city_data), "\n")
cat(
  "Mean upward mobility (kfr_pooled_p25) in", chosen_city, ":",
  fmt_num(mean(chosen_city_data$kfr_pooled_p25, na.rm = TRUE), 0), "\n"
)
cat(
  "SD upward mobility (kfr_pooled_p25) in", chosen_city, ":",
  fmt_num(sd(chosen_city_data$kfr_pooled_p25, na.rm = TRUE), 0), "\n"
)


################################################################################
# Question 2: One Tract Within the Selected City
#
# Choose one census tract in that city. Compare its upward mobility to the city
# average, then compare the city standard deviation to the state standard
# deviation.
################################################################################

# Identify the highest-mobility tract in the chosen city for the descriptive question.
chosen_tract <- chosen_city_data %>%
  filter(!is.na(kfr_pooled_p25)) %>%
  arrange(desc(kfr_pooled_p25)) %>%
  slice(1)

# Compute benchmark means/standard deviations to compare that tract to its city and state.
chosen_city_mean <- mean(chosen_city_data$kfr_pooled_p25, na.rm = TRUE)
chosen_city_sd <- sd(chosen_city_data$kfr_pooled_p25, na.rm = TRUE)
chosen_state_data <- atlas %>% filter(state == chosen_tract$state)
chosen_state_rest <- chosen_state_data %>% filter(fips != chosen_tract$fips)
chosen_state_sd <- atlas %>%
  filter(state == chosen_tract$state) %>%
  summarise(sd_state = sd(kfr_pooled_p25, na.rm = TRUE)) %>%
  pull(sd_state)

# Build the final reference table used for descriptive-statistics question 2.
tract_comparison_table <- tibble(
  `Comparison group` = c(
    paste0("Selected tract: ", chosen_tract$fips),
    chosen_city,
    "Louisiana, excluding selected tract"
  ),
  `Tracts` = c(
    1,
    nrow(chosen_city_data),
    nrow(chosen_state_rest)
  ),
  `Mean upward mobility ($)` = c(
    chosen_tract$kfr_pooled_p25,
    chosen_city_mean,
    mean(chosen_state_rest$kfr_pooled_p25, na.rm = TRUE)
  ),
  `SD upward mobility ($)` = c(
    NA_real_,
    chosen_city_sd,
    sd(chosen_state_rest$kfr_pooled_p25, na.rm = TRUE)
  ),
  `Selected tract minus group mean ($)` = c(
    0,
    chosen_tract$kfr_pooled_p25 - chosen_city_mean,
    chosen_tract$kfr_pooled_p25 - mean(chosen_state_rest$kfr_pooled_p25, na.rm = TRUE)
  )
) %>%
  mutate(
    `Mean upward mobility ($)` = fmt_num(`Mean upward mobility ($)`, 0),
    `SD upward mobility ($)` = if_else(
      is.na(`SD upward mobility ($)`),
      "N/A",
      fmt_num(`SD upward mobility ($)`, 0)
    ),
    `Selected tract minus group mean ($)` = fmt_num(`Selected tract minus group mean ($)`, 0)
  )

# Print Q2 outputs to the console so the section is fully self-contained.
cat("\n==================== Question 2 ====================\n")
cat("Selected tract FIPS:", chosen_tract$fips, "\n")
cat("Tract upward mobility ($):", fmt_num(chosen_tract$kfr_pooled_p25, 0), "\n")
cat("City mean upward mobility ($):", fmt_num(chosen_city_mean, 0), "\n")
cat("City SD ($):", fmt_num(chosen_city_sd, 0), "\n")
cat("State SD ($):", fmt_num(chosen_state_sd, 0), "\n")
cat("Tract vs. city mean ($):", fmt_num(chosen_tract$kfr_pooled_p25 - chosen_city_mean, 0), "\n\n")

# Print the formatted comparison table directly to the console.
print(tract_comparison_table)

# Render the styled kable version for the knitted document.
print(
  kable(
    tract_comparison_table,
    caption = "Selected New Orleans tract compared with New Orleans and the rest of Louisiana",
    align = c("l", "c", "r", "r", "r")
  ) %>%
    kable_styling(full_width = FALSE)
)


################################################################################
# Question 3: Poverty and Upward Mobility in the Four Cities
#
# For each of the four cities, regress child income for parents at the 25th
# percentile on the 1990 poverty rate. Use scatter plots with fitted lines to
# compare the association across cities.
################################################################################

# Fit one simple poverty-on-mobility regression per city for the multi-city comparison.
city_models <- lapply(
  setNames(cities, cities),
  function(x) lm(mobility_k ~ poverty_pp, data = filter(atlas, czname == x))
)

## ----city-scatter, fig.cap="Income of children from the 25th parental percentile against tract poverty rates, by city."----
# Visualize the city-by-city relationship between poverty and upward mobility.
q3_plot <- ggplot(city_data, aes(x = poverty_pp, y = kfr_pooled_p25)) +
  geom_point(alpha = 0.25, size = 1, color = "#1f4e79") +
  geom_smooth(method = "lm", se = FALSE, color = "#b22222", linewidth = 1) +
  facet_wrap(~ czname, scales = "free") +
  labs(
    x = "Poverty rate in 1990 (%)",
    y = "Child income for p25 parents ($)",
    title = "Higher tract poverty is associated with lower upward mobility in all four cities"
  ) +
  theme_minimal(base_size = 12)

# Print the scatter so it draws when the script is sourced.
print(q3_plot)

# Print the four city-level slopes for the inline 10-ppt comparison in the writeup.
cat("\n==================== Question 3 ====================\n")
cat("Per-city poverty slopes (mobility_k on poverty_pp), with implied 10-ppt change:\n")
for (city in cities) {
  slope <- coef(city_models[[city]])[["poverty_pp"]]
  cat(
    sprintf(
      "  %-13s slope = %s   |   10-ppt change = $%sk\n",
      city,
      fmt_num(slope, 4),
      fmt_num(10 * slope, 2)
    )
  )
}

# Print regression summaries for each city so the per-city fits are visible in the console.
for (city in cities) {
  cat("\n--- City regression summary:", city, "---\n")
  print(summary(city_models[[city]]))
}

# Tidy coefficient table across the four cities for a compact at-a-glance view.
q3_coef_table <- bind_rows(lapply(cities, function(city) {
  td <- tidy(city_models[[city]])
  tibble(
    City = city,
    Term = td$term,
    Estimate = fmt_num(td$estimate, 4),
    `Std. Error` = fmt_num(td$std.error, 4),
    `t value` = fmt_num(td$statistic, 2),
    `p value` = fmt_num(td$p.value, 4)
  )
}))
cat("\n--- Q3 tidy coefficient table across all four cities ---\n")
print(q3_coef_table, n = Inf)


################################################################################
# Question 4: Omitted Variable Bias - Racial Composition
#
# Treat racial composition as a possible omitted variable. Create the
# majority_non_white dummy, rerun the poverty regression for one city with this
# control, and use the OVB formula to compare predicted bias to the actual
# coefficient change.
################################################################################

# Subset to the question-4 city and estimate the simple and controlled models.
q4_city <- "New Orleans"
q4_data <- atlas %>% filter(czname == q4_city)
model_3 <- lm(mobility_k ~ poverty_pp, data = q4_data)
model_4 <- lm(mobility_k ~ poverty_pp + majority_non_white, data = q4_data)

# Estimate the auxiliary regression needed for the omitted-variable-bias decomposition.
aux_ovb <- lm(majority_non_white ~ poverty_pp, data = q4_data)

# Recover the OVB ingredients and compare predicted bias to the actual coefficient shift.
beta_naive <- coef(model_3)[["poverty_pp"]]
beta_controlled <- coef(model_4)[["poverty_pp"]]
delta_mnw <- coef(model_4)[["majority_non_white"]]
gamma_pov_to_mnw <- coef(aux_ovb)[["poverty_pp"]]
predicted_bias <- delta_mnw * gamma_pov_to_mnw
actual_change <- beta_naive - beta_controlled

# Print the model summaries used for the OVB walk-through.
cat("\n==================== Question 4 ====================\n")
cat("\n--- Model 3: mobility_k ~ poverty_pp (", q4_city, ") ---\n", sep = "")
print(summary(model_3))
cat("\n--- Model 4: mobility_k ~ poverty_pp + majority_non_white (", q4_city, ") ---\n", sep = "")
print(summary(model_4))
cat("\n--- Auxiliary regression: majority_non_white ~ poverty_pp ---\n")
print(summary(aux_ovb))

# Print the OVB decomposition numbers in a labeled block.
cat("\n--- OVB decomposition ---\n")
cat("beta_naive (Model 3 poverty slope):                 ", fmt_num(beta_naive, 4), "\n")
cat("beta_controlled (Model 4 poverty slope):            ", fmt_num(beta_controlled, 4), "\n")
cat("delta (Model 4 majority_non_white coefficient):     ", fmt_num(delta_mnw, 4), "\n")
cat("gamma (poverty -> majority_non_white aux slope):    ", fmt_num(gamma_pov_to_mnw, 4), "\n")
cat("Predicted bias = delta * gamma:                     ", fmt_num(predicted_bias, 4), "\n")
cat("Actual change  = beta_naive - beta_controlled:      ", fmt_num(actual_change, 4), "\n")

# Tidy side-by-side comparison of Model 3 and Model 4 coefficients for Q4 alone.
q4_compare <- tibble(
  Term = c("(Intercept)", "poverty_pp", "majority_non_white"),
  `Model 3 estimate` = c(
    fmt_num(coef(model_3)[["(Intercept)"]], 4),
    fmt_num(coef(model_3)[["poverty_pp"]], 4),
    "n/a"
  ),
  `Model 4 estimate` = c(
    fmt_num(coef(model_4)[["(Intercept)"]], 4),
    fmt_num(coef(model_4)[["poverty_pp"]], 4),
    fmt_num(coef(model_4)[["majority_non_white"]], 4)
  )
)
cat("\n--- Q4 Model 3 vs. Model 4 coefficient comparison ---\n")
print(q4_compare)


################################################################################
# Question 5: Interaction Model and Combined Regression Table
#
# Add a poverty-by-majority_non_white interaction to test whether the poverty
# slope differs in majority non-white tracts. The combined Models 3-5 table
# follows immediately so the trio reads top to bottom.
################################################################################

# Add the interaction model that the homework asks about.
model_5 <- lm(mobility_k ~ poverty_pp * majority_non_white, data = q4_data)

# Print the interaction-model summary so Q5 has its own console output.
cat("\n==================== Question 5 ====================\n")
cat("\n--- Model 5: mobility_k ~ poverty_pp * majority_non_white (", q4_city, ") ---\n", sep = "")
print(summary(model_5))

## ----models-345-table, results='asis'-----------------------------------------
# Assemble Models 3-5 into one publication-style table for the New Orleans section.
table_345 <- tibble(
  Term = c(
    "Poverty rate in 1990 (percentage points)",
    "Majority non-white tract (= 1)",
    "Poverty rate × Majority non-white",
    "Constant",
    "Observations",
    "R-squared"
  ),
  `Model 3: Poverty only` = c(
    fmt_coef(tidy(model_3)$estimate[2], tidy(model_3)$std.error[2]),
    "",
    "",
    fmt_coef(tidy(model_3)$estimate[1], tidy(model_3)$std.error[1]),
    as.character(nobs(model_3)),
    fmt_num(summary(model_3)$r.squared, 3)
  ),
  `Model 4: + Race dummy` = c(
    fmt_coef(tidy(model_4)$estimate[2], tidy(model_4)$std.error[2]),
    fmt_coef(tidy(model_4)$estimate[3], tidy(model_4)$std.error[3]),
    "",
    fmt_coef(tidy(model_4)$estimate[1], tidy(model_4)$std.error[1]),
    as.character(nobs(model_4)),
    fmt_num(summary(model_4)$r.squared, 3)
  ),
  `Model 5: + Interaction` = c(
    fmt_coef(tidy(model_5)$estimate[2], tidy(model_5)$std.error[2]),
    fmt_coef(tidy(model_5)$estimate[3], tidy(model_5)$std.error[3]),
    fmt_coef(tidy(model_5)$estimate[4], tidy(model_5)$std.error[4]),
    fmt_coef(tidy(model_5)$estimate[1], tidy(model_5)$std.error[1]),
    as.character(nobs(model_5)),
    fmt_num(summary(model_5)$r.squared, 3)
  )
)

# Print the regression tibble plainly so the values are visible in the console.
print(table_345)

# Print the regression table with the coefficient units clarified in the note.
print(
  kable(
    table_345,
    caption = "New Orleans regressions: poverty, racial composition, and heterogeneous associations with upward mobility",
    align = c("l", "c", "c", "c")
  ) %>%
    kable_styling(full_width = FALSE) %>%
    footnote(
      general = "Dependent variable is child income for parents at the 25th percentile, measured in thousands of dollars. Standard errors are in parentheses. Poverty is measured in percentage points. Majority non-white equals 1 when the tract's white share in 2000 is below 50 percent.",
      general_title = "Notes: "
    )
)

# Tidy companion view of Models 3-5 coefficients for quick console inspection.
get_coef <- function(model, term) {
  est <- coef(model)
  if (term %in% names(est)) fmt_num(est[[term]], 4) else "n/a"
}
q5_compare <- tibble(
  Term = c("(Intercept)", "poverty_pp", "majority_non_white", "poverty_pp:majority_non_white"),
  `Model 3` = sapply(c("(Intercept)", "poverty_pp", "majority_non_white", "poverty_pp:majority_non_white"),
                     get_coef, model = model_3),
  `Model 4` = sapply(c("(Intercept)", "poverty_pp", "majority_non_white", "poverty_pp:majority_non_white"),
                     get_coef, model = model_4),
  `Model 5` = sapply(c("(Intercept)", "poverty_pp", "majority_non_white", "poverty_pp:majority_non_white"),
                     get_coef, model = model_5)
)
cat("\n--- Q5 Models 3-5 coefficient comparison ---\n")
print(q5_compare)


################################################################################
# Regression Analysis
#
# Question 6:
# This question is answered in prose in the R Markdown/PDF: the models are
# associational rather than causal.
#
# Questions 7-9:
# Re-estimate the model from question 4 on all data points, then include a dummy
# variable for each commuting zone with factor(cz). This compares tracts within
# the same commuting zone instead of comparing across cities.
################################################################################

# Re-run the pooled model nationally, then add commuting-zone fixed effects.
all_base <- lm(mobility_k ~ poverty_pp + majority_non_white, data = atlas)
all_fe <- lm(mobility_k ~ poverty_pp + majority_non_white + factor(cz), data = atlas)

################################################################################
# Open Question
#
# Assignment prompt:
# Use one table, one figure, and one paragraph to answer whether
# intergenerational mobility differs between urban and rural areas.
#
# Coding choice:
# Use tract population density as the urban/rural proxy. The bottom density
# quartile is the rural proxy, the top density quartile is the urban proxy, and
# density deciles are used for the figure.
################################################################################

# Create density-based bins for the open question on urban versus rural mobility.
density_breaks <- quantile(atlas$popdensity2000, probs = seq(0, 1, 0.1), na.rm = TRUE)
atlas_open <- atlas %>%
  mutate(
    density_decile = cut(popdensity2000, breaks = density_breaks, include.lowest = TRUE, labels = 1:10),
    density_group = case_when(
      popdensity2000 <= quantile(popdensity2000, 0.25, na.rm = TRUE) ~ "Rural proxy: bottom density quartile",
      popdensity2000 >= quantile(popdensity2000, 0.75, na.rm = TRUE) ~ "Urban proxy: top density quartile",
      TRUE ~ "Middle 50%"
    )
  )

# Summarize the top- and bottom-density tracts for the open-ended comparison table.
open_table <- atlas_open %>%
  filter(density_group != "Middle 50%") %>%
  group_by(density_group) %>%
  summarise(
    Tracts = n(),
    `Mean mobility ($)` = mean(kfr_pooled_p25, na.rm = TRUE),
    `SD mobility ($)` = sd(kfr_pooled_p25, na.rm = TRUE),
    `Mean poverty rate (%)` = mean(poverty_pp, na.rm = TRUE),
    `Mean white share (%)` = mean(share_white2000 * 100, na.rm = TRUE)
  )

# Summarize each density decile so the open-question figure can trace the full gradient.
open_deciles <- atlas_open %>%
  filter(!is.na(density_decile)) %>%
  group_by(density_decile) %>%
  summarise(
    mean_density = mean(popdensity2000, na.rm = TRUE),
    mean_mobility = mean(kfr_pooled_p25, na.rm = TRUE),
    mean_poverty = mean(poverty_pp, na.rm = TRUE)
  )

################################################################################
# Instrumental Variable
#
# Assignment prompt:
# Use the Angrist and Evans fertility example. Create an instrument equal to 1
# when the first two children are the same gender. Then manually run the three
# regressions that make up 2SLS instead of using ivreg().
################################################################################

# Load the textbook fertility dataset and recode the treatment/instrument as numeric.
data("Fertility2")
fertility2 <- Fertility2 %>%
  mutate(
    morekids_num = if_else(morekids == "yes", 1, 0),
    same_gender = if_else(gender1 == gender2, 1, 0)
  )

# Walk through IV manually by estimating the first stage, reduced form, and second stage.
iv_first_stage <- lm(morekids_num ~ same_gender, data = fertility2)
iv_reduced_form <- lm(work ~ same_gender, data = fertility2)
fertility2 <- fertility2 %>% mutate(morekids_hat = fitted(iv_first_stage))
iv_second_stage <- lm(work ~ morekids_hat, data = fertility2)


################################################################################
# Regression Analysis: Questions 7-9 Fixed Effects Table
################################################################################

## ----fe-table, results='asis'-------------------------------------------------
# Tidy the national OLS and fixed-effects models before tabulating them side by side.
tidy_base <- tidy(all_base)
tidy_fe <- tidy(all_fe)

table_fe <- tibble(
  Term = c(
    "Poverty rate in 1990 (percentage points)",
    "Majority non-white tract (= 1)",
    "Commuting-zone fixed effects",
    "Constant",
    "Observations",
    "R-squared"
  ),
  `Model 4 replicated: national pooled OLS` = c(
    fmt_coef(tidy_base$estimate[2], tidy_base$std.error[2]),
    fmt_coef(tidy_base$estimate[3], tidy_base$std.error[3]),
    "No",
    fmt_coef(tidy_base$estimate[1], tidy_base$std.error[1]),
    as.character(nobs(all_base)),
    fmt_num(summary(all_base)$r.squared, 3)
  ),
  `Model 4 + commuting-zone FE` = c(
    fmt_coef(tidy_fe$estimate[2], tidy_fe$std.error[2]),
    fmt_coef(tidy_fe$estimate[3], tidy_fe$std.error[3]),
    "Yes",
    fmt_coef(tidy_fe$estimate[1], tidy_fe$std.error[1]),
    as.character(nobs(all_fe)),
    fmt_num(summary(all_fe)$r.squared, 3)
  )
)

# Print the fixed-effects comparison table for the panel-data-style extension.
kable(
  table_fe,
  caption = "National regressions with and without commuting-zone fixed effects",
  align = c("l", "c", "c")
) %>%
  kable_styling(full_width = FALSE) %>%
  footnote(
    general = "Dependent variable is child income for parents at the 25th percentile, measured in thousands of dollars. Standard errors are in parentheses. Poverty is measured in percentage points.",
    general_title = "Notes: "
  )


################################################################################
# Open Question: Table
################################################################################

## ----open-table, results='asis'-----------------------------------------------
# Format the open-question summary statistics before sending them to kable.
open_table_fmt <- open_table %>%
  mutate(across(where(is.numeric), ~ fmt_num(.x, 2)))

# Print the urban-versus-rural comparison table.
kable(
  open_table_fmt,
  caption = "Urban-versus-rural comparison using tract population density as a proxy",
  align = c("l", "c", "c", "c", "c", "c")
) %>%
  kable_styling(full_width = FALSE)


################################################################################
# Open Question: Figure
################################################################################

## ----open-figure, fig.cap="Mean upward mobility by national tract-density decile."----
# Graph the density-decile pattern to support the open-question interpretation.
ggplot(open_deciles, aes(x = as.numeric(as.character(density_decile)), y = mean_mobility)) +
  geom_line(color = "#1f4e79", linewidth = 1) +
  geom_point(color = "#b22222", size = 2) +
  scale_x_continuous(breaks = 1:10) +
  labs(
    x = "Population-density decile (1 = sparsest tracts, 10 = densest tracts)",
    y = "Mean child income for p25 parents ($)",
    title = "The densest tracts do not deliver uniformly higher upward mobility"
  ) +
  theme_minimal(base_size = 12)


################################################################################
# Instrumental Variable: Manual 2SLS Table
################################################################################

## ----iv-table, results='asis'-------------------------------------------------
# Combine the manual IV steps into one table so the logic reads top to bottom.
iv_table <- tibble(
  Term = c("Same-gender instrument", "Predicted third child", "Constant", "Observations", "R-squared"),
  `First stage: morekids on same_gender` = c(
    fmt_coef(tidy(iv_first_stage)$estimate[2], tidy(iv_first_stage)$std.error[2]),
    "",
    fmt_coef(tidy(iv_first_stage)$estimate[1], tidy(iv_first_stage)$std.error[1]),
    as.character(nobs(iv_first_stage)),
    fmt_num(summary(iv_first_stage)$r.squared, 3)
  ),
  `Reduced form: work on same_gender` = c(
    fmt_coef(tidy(iv_reduced_form)$estimate[2], tidy(iv_reduced_form)$std.error[2]),
    "",
    fmt_coef(tidy(iv_reduced_form)$estimate[1], tidy(iv_reduced_form)$std.error[1]),
    as.character(nobs(iv_reduced_form)),
    fmt_num(summary(iv_reduced_form)$r.squared, 3)
  ),
  `Second stage: work on fitted morekids` = c(
    "",
    fmt_coef(tidy(iv_second_stage)$estimate[2], tidy(iv_second_stage)$std.error[2]),
    fmt_coef(tidy(iv_second_stage)$estimate[1], tidy(iv_second_stage)$std.error[1]),
    as.character(nobs(iv_second_stage)),
    fmt_num(summary(iv_second_stage)$r.squared, 3)
  )
)

# Print the IV table and restate the first-stage and second-stage interpretation in plain English.
kable(
  iv_table,
  caption = "Manual two-stage least squares using same-sex first two children as an instrument",
  align = c("l", "c", "c", "c")
) %>%
  kable_styling(full_width = FALSE) %>%
  footnote(
    general = "The first stage shows that same-sex first two children increase the probability of having a third child by about 6.7 percentage points. The reduced form is negative, and the second-stage estimate implies that an additional child lowers maternal work in this sample.",
    general_title = "Notes: "
  )


################################################################################
# Code Understanding Sufficiency Test
#
# Assignment prompt:
# List the libraries used in the code, then list and explain 15 functions from
# those libraries in plain language.
################################################################################

## ----code-understanding-table, results='asis'---------------------------------
# End with a quick package/function glossary so Edgar can map code syntax to task steps.
code_understanding <- tibble::tribble(
  ~Package, ~Function, ~Description,
  "readr", "read_csv()", "Imports a CSV file into R as a data frame or tibble.",
  "dplyr", "mutate()", "Creates new variables or transforms existing ones.",
  "dplyr", "filter()", "Keeps only rows that satisfy a condition.",
  "dplyr", "arrange()", "Sorts rows in ascending or descending order.",
  "dplyr", "slice()", "Selects rows by their position in the data frame.",
  "dplyr", "group_by()", "Creates groups so later calculations are done within each group.",
  "dplyr", "summarise()", "Reduces each group to one or more summary statistics.",
  "ggplot2", "ggplot()", "Starts a graph by defining the dataset and aesthetics.",
  "ggplot2", "geom_point()", "Adds a scatter-plot layer.",
  "ggplot2", "geom_smooth()", "Adds a fitted line, such as a linear regression line.",
  "ggplot2", "facet_wrap()", "Splits one plot into multiple panels by category.",
  "broom", "tidy()", "Extracts model coefficients and standard errors into a tidy table.",
  "knitr", "kable()", "Creates a clean table for R Markdown output.",
  "kableExtra", "kable_styling()", "Adds formatting options to a `kable()` table.",
  "AER", "data()", "Loads a dataset that comes bundled with a package."
)

# Print the glossary table as a final reference aid.
kable(code_understanding, align = c("l", "l", "l")) %>%
  kable_styling(full_width = FALSE)
