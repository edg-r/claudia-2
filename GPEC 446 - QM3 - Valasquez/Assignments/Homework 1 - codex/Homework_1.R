################################################################################
# Setup & Table Formatting
################################################################################

#Set working directory
#setwd('/Users/edgar/Documents/01 Projects/GPEC 446 - QM3 - Valasquez/Assignments/Homework 1')

library(dplyr)
library(ggplot2)
library(readr)
library(stargazer)
library(AER)

# Define small formatting helpers up front so every table uses the same style
fmt_num <- function(x, digits = 2) formatC(x, format = "f", digits = digits, big.mark = ",")
fmt_coef <- function(est, se, digits = 3) sprintf("%s (%s)", fmt_num(est, digits), fmt_num(se, digits))

html_escape <- function(x) {
  x <- as.character(x)
  x <- gsub("&", "&amp;", x, fixed = TRUE)
  x <- gsub("<", "&lt;", x, fixed = TRUE)
  x <- gsub(">", "&gt;", x, fixed = TRUE)
  x
}

write_assignment_table <- function(data, caption, file, notes = NULL) {
  # Keep non-regression exports visually consistent with the regression tables
  # while writing compact standalone HTML files
  data <- as.data.frame(data, stringsAsFactors = FALSE)
  ncols <- ncol(data)
  header <- paste0(
    "<tr><td colspan=\"", ncols, "\" style=\"border-bottom: 1px solid black\"></td></tr>",
    "<tr>",
    paste(sprintf("<td>%s</td>", html_escape(names(data))), collapse = ""),
    "</tr>",
    "<tr><td colspan=\"", ncols, "\" style=\"border-bottom: 1px solid black\"></td></tr>"
  )
  body <- paste(
    apply(data, 1, function(row) {
      cells <- vapply(seq_along(row), function(i) {
        align <- if (i == 1) "left" else "center"
        sprintf("<td style=\"text-align:%s\">%s</td>", align, html_escape(row[[i]]))
      }, character(1))
      paste0("<tr>", paste(cells, collapse = ""), "</tr>")
    }),
    collapse = "\n"
  )
  note_rows <- character(0)
  if (!is.null(notes)) {
    note_rows <- paste0(
      "<tr><td colspan=\"", ncols, "\" style=\"border-bottom: 1px solid black\"></td></tr>",
      paste(
        sprintf(
          "<tr><td style=\"text-align:left\"><em>Note:</em></td><td colspan=\"%s\" style=\"text-align:right\">%s</td></tr>",
          ncols - 1,
          html_escape(notes)
        ),
        collapse = "\n"
      )
    )
  }
  html <- paste0(
    "\n<table style=\"text-align:center\"><caption><strong>", html_escape(caption), "</strong></caption>\n",
    header, "\n",
    body, "\n",
    note_rows, "\n",
    "</table>\n"
  )
  writeLines(html, file)
}


################################################################################
# Load Opportunity Atlas from csv
################################################################################

# Load the main tract-level dataset and construct the variables used across questions
atlas <- read_csv("atlas.csv", show_col_types = FALSE) %>%
  mutate(
    # Regression questions 4-5: create the required majority-non-white dummy
    majority_non_white = if_else(share_white2000 < 0.5, 1, 0, missing = NA_integer_),
    # Regression questions 3-9: put poverty on a percentage-point scale
    poverty_pp = poor_share1990 * 100,
    # Regression tables: express child income in thousands of dollars
    mobility_k = kfr_pooled_p25 / 1000,
    # Descriptive statistics question 2: build the tract FIPS code used on the map
    tract_code = sprintf("%06d", as.integer(round(tract))),
    fips = sprintf("%02d%03d%s", as.integer(state), as.integer(county), tract_code)
  )

################################################################################
# Descriptive Statistics
################################################################################

# Isolate the four cities used in the comparative scatterplot exercise
cities <- c("Los Angeles", "New York", "Chicago", "New Orleans")
city_data <- atlas %>% filter(czname %in% cities)

# Focus the tract-level descriptive work on the city chosen for the homework narrative
chosen_city <- "New Orleans"
chosen_city_data <- atlas %>% filter(czname == chosen_city)

# Identify the highest-mobility tract in the chosen city for the descriptive question
chosen_tract <- chosen_city_data %>%
  filter(!is.na(kfr_pooled_p25)) %>%
  arrange(desc(kfr_pooled_p25)) %>%
  slice(1)

# Compute benchmark means/standard deviations to compare that tract to its city and state
chosen_city_mean <- mean(chosen_city_data$kfr_pooled_p25, na.rm = TRUE)
chosen_city_sd <- sd(chosen_city_data$kfr_pooled_p25, na.rm = TRUE)
chosen_state_data <- atlas %>% filter(state == chosen_tract$state)
chosen_state_rest <- chosen_state_data %>% filter(fips != chosen_tract$fips)
chosen_state_sd <- atlas %>%
  filter(state == chosen_tract$state) %>%
  summarise(sd_state = sd(kfr_pooled_p25, na.rm = TRUE)) %>%
  pull(sd_state)

# Build the final reference table used for descriptive-statistics questions 1-2
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

print(tract_comparison_table)

# Save the descriptive table as a standalone HTML file for easy viewing/import
write_assignment_table(
  tract_comparison_table,
  caption = "Selected New Orleans tract compared with New Orleans and the rest of Louisiana",
  file = "table_q12.html"
)

################################################################################
# Regression Analysis Q3
################################################################################

# Fit one simple poverty-on-mobility regression per city for the multi-city comparison
city_models <- lapply(
  setNames(cities, cities),
  function(x) lm(mobility_k ~ poverty_pp, data = filter(atlas, czname == x))
)
reg_la <- city_models[["Los Angeles"]]
reg_ny <- city_models[["New York"]]
reg_chi <- city_models[["Chicago"]]
reg_no <- city_models[["New Orleans"]]

# Visualize the city-by-city relationship between poverty and upward mobility
city_poverty_plot <- ggplot(city_data, aes(x = poverty_pp, y = kfr_pooled_p25)) +
  geom_point(alpha = 0.25, size = 1, color = "#1f4e79") +
  geom_smooth(method = "lm", se = FALSE, color = "#b22222", linewidth = 1) +
  facet_wrap(~ czname, scales = "free") +
  labs(
    x = "Poverty rate in 1990 (%)",
    y = "Child income for p25 parents ($)",
    title = "Higher tract poverty is associated with lower upward mobility in all four cities"
  ) +
  theme_minimal(base_size = 12)

print(city_poverty_plot)

# Save the city scatterplot
ggsave(
  filename = "city_poverty_mobility.png",
  plot = city_poverty_plot,
  width = 10,
  height = 6,
  dpi = 300
)

# Export the four city regressions as a standalone stargazer HTML table
stargazer(
  reg_la,
  reg_ny,
  reg_chi,
  reg_no,
  type = "html",
  out = "table_q3.html",
  title = "Poverty and Mobility: Simple Regressions by City",
  column.labels = c("Los Angeles", "New York", "Chicago", "New Orleans"),
  dep.var.labels = "Child income at p25 ($1000s)",
  covariate.labels = c("Poverty rate in 1990 (pp)"),
  omit.stat = c("f", "ser")
)

################################################################################
# Regression Analysis Q4-5
################################################################################

# Subset to the question-4 city and estimate the three New Orleans models
q4_city <- "New Orleans"
q4_data <- atlas %>% filter(czname == q4_city)
model_3 <- lm(mobility_k ~ poverty_pp, data = q4_data)
model_4 <- lm(mobility_k ~ poverty_pp + majority_non_white, data = q4_data)
model_5 <- lm(mobility_k ~ poverty_pp * majority_non_white, data = q4_data)

# Estimate the auxiliary regression needed for the omitted-variable-bias decomposition
aux_ovb <- lm(majority_non_white ~ poverty_pp, data = q4_data)

# Recover the OVB ingredients and compare predicted bias to the actual coefficient shift
beta_naive <- coef(model_3)[["poverty_pp"]]
beta_controlled <- coef(model_4)[["poverty_pp"]]
delta_mnw <- coef(model_4)[["majority_non_white"]]
gamma_pov_to_mnw <- coef(aux_ovb)[["poverty_pp"]]
predicted_bias <- delta_mnw * gamma_pov_to_mnw
actual_change <- beta_naive - beta_controlled

ovb_summary_table <- tibble(
  Quantity = c(
    "Naive poverty coefficient",
    "Controlled poverty coefficient",
    "Effect of majority non-white dummy",
    "Auxiliary slope: majority non-white on poverty",
    "Predicted omitted-variable bias",
    "Actual coefficient change"
  ),
  Value = c(
    beta_naive,
    beta_controlled,
    delta_mnw,
    gamma_pov_to_mnw,
    predicted_bias,
    actual_change
  )
) %>%
  mutate(Value = fmt_num(Value, 3))

print(ovb_summary_table)

write_assignment_table(
  ovb_summary_table,
  caption = "New Orleans omitted-variable-bias calculation",
  file = "table_q4_ovb.html"
)

# Print and export Models 3-5 using stargazer, matching the earlier table workflow.
stargazer(
  model_3,
  model_4,
  model_5,
  type = "html",
  out = "table_q5.html",
  title = "New Orleans: Poverty, Race, and Upward Mobility",
  column.labels = c("Poverty only", "+ Race dummy", "+ Interaction"),
  dep.var.labels = "Child income at p25 ($1000s)",
  covariate.labels = c(
    "Poverty rate in 1990 (pp)",
    "Majority non-white tract (= 1)",
    "Poverty rate x Majority non-white"
  ),
  omit.stat = c("f", "ser")
)

################################################################################
# Regression Analysis Q6-7
################################################################################

# Re-run the pooled model nationally, then add commuting-zone fixed effects.
all_base <- lm(mobility_k ~ poverty_pp + majority_non_white, data = atlas)
all_fe <- lm(mobility_k ~ poverty_pp + majority_non_white + factor(cz), data = atlas)

################################################################################
# Open Question
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

# Add a regression check using the same urban/rural proxy as the table.
# The sample is restricted to the bottom and top density quartiles so the
# coefficient reads as urban-proxy tracts relative to rural-proxy tracts.
open_reg_data <- atlas_open %>%
  filter(density_group != "Middle 50%") %>%
  mutate(
    urban_proxy = if_else(density_group == "Urban proxy: top density quartile", 1, 0)
  )

open_reg_simple <- lm(mobility_k ~ urban_proxy, data = open_reg_data)
open_reg_controls <- lm(
  mobility_k ~ urban_proxy + poverty_pp + majority_non_white,
  data = open_reg_data
)
open_reg_fe <- lm(
  mobility_k ~ urban_proxy + poverty_pp + majority_non_white + factor(cz),
  data = open_reg_data
)



################################################################################
# Regression Analysis: Questions 7-9 Fixed Effects Table
################################################################################

# Print and export the fixed-effects comparison table using the same regression
# table format as the other OLS model outputs.
stargazer(
  all_base,
  all_fe,
  type = "html",
  out = "table_q79.html",
  title = "National Sample: Pooled OLS vs. Commuting-Zone Fixed Effects",
  column.labels = c("Pooled OLS", "+ CZ Fixed Effects"),
  dep.var.labels = "Child income at p25 ($1000s)",
  covariate.labels = c(
    "Poverty rate in 1990 (pp)",
    "Majority non-white tract (= 1)"
  ),
  omit = "factor\\(cz\\)",
  omit.stat = c("f", "ser"),
  add.lines = list(c("Commuting-zone fixed effects", "No", "Yes")),
  notes = c(
    "CZ fixed effects omitted from display.",
    "Column (2) identifies associations using within-CZ tract differences."
  )
)

################################################################################
# Open Question: Regression Table
################################################################################

# Export the open-question regression in the same format as the other regression
# tables. This supplements the required table, figure, and paragraph.
stargazer(
  open_reg_simple,
  open_reg_controls,
  open_reg_fe,
  type = "html",
  out = "table_open_urban_rural_regression.html",
  title = "Urban/Rural Proxy and Upward Mobility",
  column.labels = c("Urban proxy only", "+ Controls", "+ CZ Fixed Effects"),
  dep.var.labels = "Child income at p25 ($1000s)",
  covariate.labels = c(
    "Urban proxy: top density quartile",
    "Poverty rate in 1990 (pp)",
    "Majority non-white tract (= 1)"
  ),
  omit = "factor\\(cz\\)",
  omit.stat = c("f", "ser"),
  add.lines = list(c("Commuting-zone fixed effects", "No", "No", "Yes")),
  notes = c(
    "Sample restricted to top and bottom population-density quartiles.",
    "Urban proxy equals 1 for top-density-quartile tracts and 0 for bottom-density-quartile tracts."
  )
)


################################################################################
# Open Question: Graph
################################################################################

# Graph the density-decile pattern to support the open-question interpretation.
urban_density_plot <- ggplot(open_deciles, aes(x = as.numeric(as.character(density_decile)), y = mean_mobility)) +
  geom_line(color = "#1f4e79", linewidth = 1) +
  geom_point(color = "#b22222", size = 2) +
  scale_x_continuous(breaks = 1:10) +
  labs(
    x = "Population-density decile (1 = sparsest tracts, 10 = densest tracts)",
    y = "Mean child income for p25 parents ($)",
    title = "The densest tracts do not deliver uniformly higher upward mobility"
  ) +
  theme_minimal(base_size = 12)

print(urban_density_plot)

#saves urban density plot
ggsave(
  filename = "urban_density_deciles.png",
  plot = urban_density_plot,
  width = 8,
  height = 5,
  dpi = 300
)


################################################################################
# Instrumental Variable: Manual 2SLS Table
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

# Print and export the IV table in the same regression-table format as the OLS
# tables above. This keeps the manual first stage, reduced form, and fitted-value
# second stage visible while preserving consistent formatting.
stargazer(
  iv_first_stage,
  iv_reduced_form,
  iv_second_stage,
  type = "html",
  out = "table_iv_manual_2sls.html",
  title = "Manual 2SLS: Same-Sex Instrument for Third Child",
  column.labels = c("First Stage", "Reduced Form", "Manual Second Stage"),
  dep.var.labels = c("More kids", "Work", "Work"),
  covariate.labels = c(
    "Same-gender instrument",
    "Predicted third child"
  ),
  omit.stat = c("f", "ser"),
  notes = c(
    "Manual second-stage point estimate uses fitted morekids from the first stage.",
    "Manual second-stage standard errors are not corrected IV standard errors."
  )
)


################################################################################
# Code Understanding Sufficiency Test
################################################################################

# End with a package/function glossary so the code syntax can be explained in
# plain language.
code_understanding <- tibble(
  Package = c(
    "readr", "dplyr", "dplyr", "dplyr", "dplyr",
    "dplyr", "dplyr", "dplyr", "ggplot2", "ggplot2",
    "ggplot2", "ggplot2", "base R", "stargazer", "AER"
  ),
  Function = c(
    "read_csv()", "mutate()", "if_else()", "filter()", "arrange()",
    "slice()", "summarise()", "pull()", "ggplot()", "geom_point()",
    "geom_smooth()", "ggsave()", "sprintf()", "stargazer()", "data()"
  ),
  Description = c(
    "Imports a CSV file into R as a data frame or tibble.",
    "Creates new variables or transforms existing ones.",
    "Creates a conditional variable using if/else logic.",
    "Keeps only rows that satisfy a condition.",
    "Sorts rows in ascending or descending order.",
    "Selects rows by their position in the data frame.",
    "Reduces data to summary statistics.",
    "Extracts one column from a data frame as a vector or single value.",
    "Starts a graph by defining the dataset and aesthetics.",
    "Adds a scatter-plot layer.",
    "Adds a fitted line, such as a linear regression line.",
    "Saves a ggplot object as an image file.",
    "Formats numbers or text, such as padding FIPS code pieces with zeros.",
    "Creates regression tables with coefficients, standard errors, and model statistics.",
    "Loads a dataset that comes bundled with a package."
  )
)

print(code_understanding)

write_assignment_table(
  code_understanding,
  caption = "Code understanding reference",
  file = "table_code_understanding.html"
)
