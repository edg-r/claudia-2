# Week 5 Lab Script (what this file runs)
# Omitted variable bias (missing factor that affects results)
# GPCO 454 - Quantitative Methods II (course name)
# Author (who wrote it): Nico Ravanilla and David L. Vargas
# Date (when written): February 7, 2025

# ==========================================================
# 1. Preparing, Cleaning, and Organizing Data (set up and combine data)
# ==========================================================

# Working directory (folder R uses for files)
setwd("~/Desktop/QM2 R Materials/Week 5")
getwd() # Current directory (check it is correct)

# Packages to install (extra tools for R; uncomment if needed)
install.packages("patchwork") # Plot panels (arrange multiple plots)

# Load packages (bring tools into R)
library(tidyverse) # Data wrangling (clean and reshape data)
library(readxl) # Excel import (read .xlsx files)
library(stargazer) # Regression tables (nice model output)
library(ggplot2) # Plotting (make graphs)

# Load datasets (read Excel files)
gdp_data <- read_excel("county level annual GDP by industry.xlsx") # GDP by county (economic data)
demographics_data <- read_excel("county level population, poverty and education data.xlsx") # Demographics (population/poverty/education)

# GeoFIPS type (make both keys text so they match)
gdp_data <- gdp_data %>% mutate(GeoFIPS = as.character(GeoFIPS))
demographics_data <- demographics_data %>% mutate(GeoFIPS = as.character(GeoFIPS))

# Merge datasets (combine on GeoFIPS)
merged_data <- gdp_data %>%
  left_join(demographics_data, by = "GeoFIPS")

# Data preview (quick checks; commented out)
# str(merged_data)  # Structure (column types)
# head(merged_data)  # First rows (sample view)

# ==========================================================
# 2. Data Cleaning and Transformation (fix and reshape data)
# ==========================================================

# Drop duplicate column and rename (clean up names)
merged_data <- merged_data %>%
  select(-GeoName.y) %>% # Drop column (remove duplicate)
  rename(GeoName = GeoName.x) # Rename column (use clearer name)

# Filter rural counties (keep code 9 only)
filtered_data <- merged_data %>%
  filter(Rural_Urban_Continuum_Code_2023 == 9) # Code 9 (most rural)

# Drop rural code (no longer needed)
filtered_data <- filtered_data %>%
  select(-Rural_Urban_Continuum_Code_2023)

# Year columns (list of 2001 to 2023)
year_columns <- as.character(2001:2023) # Column names (years as text)

# Replace suppressed values and convert to numbers
working_data <- filtered_data %>%
  mutate(across(all_of(year_columns), ~ ifelse(.x == "(D)", NA, .x))) %>% # Suppressed value ("(D)" becomes NA)
  mutate(across(all_of(year_columns), as.numeric)) # Numeric conversion (text to numbers)

# Per capita GDP (divide by population)
working_data <- working_data %>%
  mutate(across(all_of(year_columns), ~ round(.x / POP_ESTIMATE_2023, 2))) # Round (2 decimals)


# ==========================================================
# 3. Plotting: Average GDP Per Capita Over Time for Selected Industries (make trend chart)
# ==========================================================

# NAICS codes (industry IDs)
selected_naics <- c("11", "31-33", "54,55,56", "92") # Selecting Agriculture/Manufacturing/Prof Services/Government
#selects these industries and converts to one vector

# Filter industries (keep selected codes)
selected_industry_data <- working_data %>%
  filter(IndustryClassification %in% selected_naics) # Match list (keep these)
# filter industry classification in the industries vector above

# Long format and averages (reshape and summarize)
industry_summary <- selected_industry_data %>%
  pivot_longer(cols = all_of(year_columns), names_to = "Year", values_to = "GDP_per_capita") %>%
  group_by(Year, IndustryClassification) %>%
  summarize(avg_gdp_per_capita = mean(GDP_per_capita, na.rm = TRUE), .groups = "drop")
#allows us to create a unique table that shows for each year the average gdp for each in selected_naics sector 

# Year as number (for x-axis order)
industry_summary <- industry_summary %>%
  mutate(Year = as.numeric(Year))

# Create plot (line chart)
plot_industries <- ggplot(industry_summary, aes(x = Year, y = avg_gdp_per_capita, color = IndustryClassification)) +
  geom_line(size = 1.2) +
  labs(
    title = "Average GDP Per Capita Over Time for Selected Industries",
    x = "Year",
    y = "Average GDP Per Capita (Thousand USD)",
    color = "Industry Category"
  ) +
  scale_color_manual(
    values = c("11" = "green", "31-33" = "blue", "54,55,56" = "red", "92" = "purple"),
    labels = c(
      "11" = "Agriculture, forestry, fishing and hunting",
      "31-33" = "Manufacturing",
      "54,55,56" = "Professional and business services",
      "92" = "Government and government enterprises"
    )
  ) +
  theme_minimal() +
  scale_x_continuous(breaks = 2001:2023) + # X-axis breaks (show every year)
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    plot.title = element_text(size = 12)
  )

# Show plot (draw to screen)
print(plot_industries)

# Save plot (commented out)
# ggsave("average_gdp_per_capita_selected_industries.png", plot = plot_industries, width = 10, height = 6)


# ==========================================================
# 4. Multivariate Regression Models (run several regressions)
# ==========================================================

# Regression output package (tables)
library(stargazer)

# Education shares (calculates percent of population for each of these levels of education)
regression_data <- working_data %>%
  mutate(
    Less_than_HS_Share = `Less than a high school diploma, 2018-22` / POP_ESTIMATE_2023 * 100,
    HS_Only_Share = `High school diploma only, 2018-22` / POP_ESTIMATE_2023 * 100,
    Some_College_Share = `Some college or associate's degree, 2018-22` / POP_ESTIMATE_2023 * 100,
    Bachelors_or_Higher_Share = `Bachelor's degree or higher, 2018-22` / POP_ESTIMATE_2023 * 100
  )

# Outcome variables (industry codes)
# Creates a list/dictionary, which if we go and look for agri it will tell us its 11 etc.
outcome_variables <- list(
  Agriculture = "11",
  Manufacturing = "31-33",
  ProfServices = "54,55,56",
  Government = "92"
)

# Model list (store results)
# creates empty box for models to load into
all_models <- list()

# Model labels (titles per outcome)
model_labels <- c()

# Loop over outcomes (run models for each industry)
# for every run from the list, we replace the naics_code. as we filter the data on this in the next regression
for (outcome_name in names(outcome_variables)) {
  naics_code <- outcome_variables[[outcome_name]]

  # Filter and select (data for current industry)
  #run a regression between GDP and PCTPOVALL_2021, controlled for education in region
  #model data filtered by industry
  model_data <- regression_data %>%
    filter(IndustryClassification == naics_code) %>% #takes the naics_code from the for loop, and runs regression again
    select(`2023`, PCTPOVALL_2021, Less_than_HS_Share, HS_Only_Share, Some_College_Share, Bachelors_or_Higher_Share, `2022`)

  
  # Models run successivley, to compare
  # Model 1 (poverty only)
  model_1 <- lm(`2023` ~ PCTPOVALL_2021, data = model_data)

  # Model 2 (poverty + education)
  model_2 <- lm(`2023` ~ PCTPOVALL_2021 + Less_than_HS_Share + HS_Only_Share +
    Some_College_Share + Bachelors_or_Higher_Share, data = model_data)

  # Model 3 (add prior year GDP)
  model_3 <- lm(`2023` ~ PCTPOVALL_2021 + Less_than_HS_Share + HS_Only_Share +
    Some_College_Share + Bachelors_or_Higher_Share + `2022`, data = model_data)

  # Store models (collect results)
  # to prevent overwriting, we append and just add what we have to whatever we had before
  all_models <- append(all_models, list(model_1, model_2, model_3))

  # Store labels (repeat outcome name)
  # appends all labels to not get overflow 
  model_labels <- append(model_labels, c(outcome_name, outcome_name, outcome_name))
}

# Stargazer output (save regression table)
stargazer(
  all_models,
  type = "html",
  title = "Regression Results: Effects of Poverty and Education on GDP (2023)",
  dep.var.labels = "GDP Per Capita (2023)",
  covariate.labels = c(
    "Poverty Rate (2021)",
    "Share with Less than High School",
    "Share with High School Only",
    "Share with Some College",
    "Share with Bachelor's Degree or Higher",
    "GDP Per Capita (2022)"
  ),
  column.labels = model_labels,
  align = TRUE,
  no.space = TRUE,
  digits = 2,
  out = "regression_results.txt"
)

# ==================================
# 5. Detecting Omitted Variable Bias
# ==================================
# Combine residual plots into one plot to check ommited variable bias

# Load necessary package for plots
library(patchwork) # For arranging plots in panels

# Create residual plots for each model and save them
for (outcome_name in names(outcome_variables)) {
  naics_code <- outcome_variables[[outcome_name]]
  
  # Filter data for the current industry
  model_data <- regression_data %>%
    filter(IndustryClassification == naics_code)
  
  # Remove rows with any NA values in the relevant columns before fitting models
  model_data <- model_data %>%
    drop_na(`2023`, PCTPOVALL_2021, Less_than_HS_Share, HS_Only_Share, Some_College_Share, Bachelors_or_Higher_Share, `2022`)
  
  # Refit models to extract residuals and add them to model_data
  model_data <- model_data %>%
    mutate(
      residuals_model_1 = residuals(lm(`2023` ~ PCTPOVALL_2021, data = model_data)),
      residuals_model_2 = residuals(lm(`2023` ~ PCTPOVALL_2021 + Less_than_HS_Share + HS_Only_Share +
                                         Some_College_Share + Bachelors_or_Higher_Share, data = model_data)),
      residuals_model_3 = residuals(lm(`2023` ~ PCTPOVALL_2021 + Less_than_HS_Share + HS_Only_Share +
                                         Some_College_Share + Bachelors_or_Higher_Share + `2022`, data = model_data))
    )
  
  # Generate residual plots for each model
  residual_plot_1 <- ggplot(model_data, aes(x = PCTPOVALL_2021, y = residuals_model_1)) +
    geom_point() +
    ## adds dashed line around 0, if it is omitted random, it should be random around 0
    geom_hline(yintercept = 0, linetype = "dashed") +
    labs(
      title = paste(outcome_name, "Model 1 Residuals"),
      x = "Poverty Rate (2021)",
      y = "Residuals"
    ) +
    theme_minimal()
  
  residual_plot_2 <- ggplot(model_data, aes(x = PCTPOVALL_2021, y = residuals_model_2)) +
    geom_point() +
    geom_hline(yintercept = 0, linetype = "dashed") +
    labs(
      title = paste(outcome_name, "Model 2 Residuals"),
      x = "Poverty Rate (2021)",
      y = "Residuals"
    ) +
    theme_minimal()
  
  residual_plot_3 <- ggplot(model_data, aes(x = PCTPOVALL_2021, y = residuals_model_3)) +
    geom_point() +
    geom_hline(yintercept = 0, linetype = "dashed") +
    labs(
      title = paste(outcome_name, "Model 3 Residuals"),
      x = "Poverty Rate (2021)",
      y = "Residuals"
    ) +
    theme_minimal()
  
  # Arrange the three plots in a panel
  combined_plot <- residual_plot_1 / residual_plot_2 / residual_plot_3
  
  # Print the plot to the console
  print(combined_plot)
  
  
  # Save the panel plot to a PNG file
  ggsave(
    filename = paste0("residual_plots_", outcome_name, ".png"),
    plot = combined_plot,
    width = 10,
    height = 12
  )
}

