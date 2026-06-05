# ==============================================================================
# GPEC 446 Data Project: Speed Limits and Traffic Fatalities Analysis
# Author: Tyche (Class Agent)
# Date: 2026-06-04
# Target: Test driver attentiveness vs. kinetic severity hypothesis of speed limits
# ==============================================================================

rm(list = ls())

# Load required packages
library(sandwich)
library(lmtest)
library(stargazer)
library(ggplot2)

# ------------------------------------------------------------------------------
# 1. Load and Clean Dataset
# ------------------------------------------------------------------------------

# Handle portable pathing for the traffic fatalities dataset
if (file.exists("traffic_fat.Rda")) {
  load("traffic_fat.Rda")
} else if (file.exists("../traffic_fat.Rda")) {
  load("../traffic_fat.Rda")
} else {
  load("/Users/edgar/Documents/000 Files/02 Areas/UCSD/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez/Assignments/Data Project/traffic_fat.Rda")
}
data <- traffic_fat

# Sort panel by state name and year
data <- data[order(data$name, data$year), ]

# ------------------------------------------------------------------------------
# 2. Variable Construction
# ------------------------------------------------------------------------------

# Construct outcome rates per 100,000 population
data$fatalities_per_100k <- (data$totfat / data$totpop) * 100000
data$occfat_per_100k <- (data$occfat / data$totpop) * 100000
data$noccfat_per_100k <- (data$noccfat / data$totpop) * 100000

# Construct log transformations
data$log_totfat <- log(data$totfat)
data$log_pop <- log(data$totpop)

# Construct total VMT control in billions (vmturb + vmtrur)
# Note: DC has NA for vmtrur, so total_vmt will be NA for DC.
data$total_vmt <- data$vmturb + data$vmtrur

# ------------------------------------------------------------------------------
# 3. Model Estimation
# ------------------------------------------------------------------------------

# Model 1: Naive OLS (Overall Fatality Rate per 100k)
m1 <- lm(
  fatalities_per_100k ~ lim70 + sbprim + sbsec + bac08 + mlda21 + pcinc + unemprte + total_vmt,
  data = data
)

# Model 2: TWFE (Overall Fatality Rate per 100k, FE only)
m2 <- lm(
  fatalities_per_100k ~ lim70 + factor(name) + factor(year),
  data = data
)

# Model 3: TWFE (Overall Fatality Rate per 100k, Full Controls)
m3 <- lm(
  fatalities_per_100k ~ lim70 + sbprim + sbsec + bac08 + mlda21 + pcinc + unemprte + total_vmt + factor(name) + factor(year),
  data = data
)

# Model 4: TWFE (Log Total Fatalities, Full Controls)
m4 <- lm(
  log_totfat ~ lim70 + sbprim + sbsec + bac08 + mlda21 + pcinc + unemprte + total_vmt + log_pop + factor(name) + factor(year),
  data = data
)

# Model 5: TWFE (Occupant Fatality Rate per 100k, Full Controls)
m5 <- lm(
  occfat_per_100k ~ lim70 + sbprim + sbsec + bac08 + mlda21 + pcinc + unemprte + total_vmt + factor(name) + factor(year),
  data = data
)

# Model 6: TWFE (Non-occupant Fatality Rate per 100k, Full Controls)
m6 <- lm(
  noccfat_per_100k ~ lim70 + sbprim + sbsec + bac08 + mlda21 + pcinc + unemprte + total_vmt + factor(name) + factor(year),
  data = data
)

# ------------------------------------------------------------------------------
# 4. Standard Error Clustering at the State Level
# ------------------------------------------------------------------------------

# Helper functions to extract state-clustered robust standard errors and p-values
get_clustered_se <- function(model) {
  vcov_clustered <- vcovCL(model, cluster = ~name)
  sqrt(diag(vcov_clustered))
}

get_clustered_p <- function(model) {
  coeftest_output <- coeftest(model, vcov = vcovCL(model, cluster = ~name))
  coeftest_output[, "Pr(>|t|)"]
}

# Compile clustered standard errors and p-values lists for stargazer
se_list <- list(
  get_clustered_se(m1),
  get_clustered_se(m2),
  get_clustered_se(m3),
  get_clustered_se(m4),
  get_clustered_se(m5),
  get_clustered_se(m6)
)

p_list <- list(
  get_clustered_p(m1),
  get_clustered_p(m2),
  get_clustered_p(m3),
  get_clustered_p(m4),
  get_clustered_p(m5),
  get_clustered_p(m6)
)

# ------------------------------------------------------------------------------
# 5. Export Stargazer Regression Table
# ------------------------------------------------------------------------------

stargazer(
  m1, m2, m3, m4, m5, m6,
  type = "html",
  se = se_list,
  p = p_list,
  out = "speed_limit_fatalities_tables.html",
  title = "Table 1: Speed Limits (lim70) and Traffic Fatalities",
  column.labels = c(
    "Rate Naive OLS", "Rate FE Only", "Rate FE Controls", 
    "Log Fatalities FE", "Occupant Rate FE", "Non-occupant Rate FE"
  ),
  dep.var.labels.include = FALSE,
  covariate.labels = c(
    "70 mph Speed Limit (lim70)",
    "Primary seatbelt law",
    "Secondary seatbelt law",
    "0.08 BAC law",
    "Minimum drinking age 21",
    "Per-capita income",
    "Unemployment rate",
    "Total VMT (billions)",
    "Log population"
  ),
  omit = "factor",
  omit.labels = NULL,
  add.lines = list(
    c("State Fixed Effects", "No", "Yes", "Yes", "Yes", "Yes", "Yes"),
    c("Year Fixed Effects", "No", "Yes", "Yes", "Yes", "Yes", "Yes")
  ),
  keep.stat = c("n", "rsq", "adj.rsq"),
  notes = "Standard errors are clustered at the state level (reported in parentheses). The dependent variables are rates per 100,000 population, except for Column 4 which is the log of total fatalities. All models include state and year fixed effects except Column 1. Column 4 controls for Log population."
)

# ------------------------------------------------------------------------------
# 6. Export Text Regression Summaries
# ------------------------------------------------------------------------------

sink("speed_limit_fatalities_summaries.txt")
cat("Speed Limits (lim70) and Traffic Fatalities Analysis\n")
cat("====================================================\n")
cat("Generated by: Tyche\n")
cat("Date: 2026-06-04\n\n")

cat("SAMPLE INFORMATION:\n")
cat("Total observations:", nrow(data), "\n")
cat("Complete cases in Model 3 (TWFE with Controls):", sum(complete.cases(data[, c("fatalities_per_100k", "lim70", "sbprim", "sbsec", "bac08", "mlda21", "pcinc", "unemprte", "total_vmt", "name", "year")])), "\n")
cat("DC is excluded in control models due to missing rural mileage/VMT.\n\n")

cat("REGRESSION COEFFICIENTS ON lim70 (STATE-CLUSTERED SE):\n")
models_list <- list(
  "Model 1: Naive OLS (Rate per 100k)" = m1,
  "Model 2: TWFE Only (Rate per 100k)" = m2,
  "Model 3: TWFE with Controls (Rate per 100k)" = m3,
  "Model 4: TWFE with Controls (Log Fatalities)" = m4,
  "Model 5: TWFE with Controls (Occupant Rate)" = m5,
  "Model 6: TWFE with Controls (Non-occupant Rate)" = m6
)

for (name_m in names(models_list)) {
  m <- models_list[[name_m]]
  ct <- coeftest(m, vcov = vcovCL(m, cluster = ~name))
  cat("\n", name_m, ":\n", sep = "")
  print(ct["lim70", , drop=FALSE])
}
sink()

# ------------------------------------------------------------------------------
# 7. Event-Study Model Construction & Estimation
# ------------------------------------------------------------------------------

# Identify first year of lim70 adoption for treated states
adoption_years <- aggregate(year ~ name, data = data[data$lim70 == 1, ], FUN = min)
names(adoption_years) <- c("name", "first_year_lim70")
data <- merge(data, adoption_years, by = "name", all.x = TRUE)

# Calculate relative year
data$rel_year <- data$year - data$first_year_lim70

# Construct event study lead/lag dummies (reference year k = -1 is omitted)
event_vars <- c(
  "lead_6_plus", "lead_5", "lead_4", "lead_3", "lead_2", 
  "lag_0", "lag_1", "lag_2", "lag_3", "lag_4", "lag_5", "lag_6_plus"
)

for (v in event_vars) {
  data[[v]] <- 0
}

# Assign values for treated states based on rel_year (control states stay 0)
data$lead_6_plus[!is.na(data$rel_year) & data$rel_year <= -6] <- 1
data$lead_5[!is.na(data$rel_year) & data$rel_year == -5] <- 1
data$lead_4[!is.na(data$rel_year) & data$rel_year == -4] <- 1
data$lead_3[!is.na(data$rel_year) & data$rel_year == -3] <- 1
data$lead_2[!is.na(data$rel_year) & data$rel_year == -2] <- 1
data$lag_0[!is.na(data$rel_year) & data$rel_year == 0] <- 1
data$lag_1[!is.na(data$rel_year) & data$rel_year == 1] <- 1
data$lag_2[!is.na(data$rel_year) & data$rel_year == 2] <- 1
data$lag_3[!is.na(data$rel_year) & data$rel_year == 3] <- 1
data$lag_4[!is.na(data$rel_year) & data$rel_year == 4] <- 1
data$lag_5[!is.na(data$rel_year) & data$rel_year == 5] <- 1
data$lag_6_plus[!is.na(data$rel_year) & data$rel_year >= 6] <- 1

# Estimate Event-Study Model for Overall Fatality Rate
es_model <- lm(
  fatalities_per_100k ~ lead_6_plus + lead_5 + lead_4 + lead_3 + lead_2 +
    lag_0 + lag_1 + lag_2 + lag_3 + lag_4 + lag_5 + lag_6_plus +
    sbprim + sbsec + bac08 + mlda21 + pcinc + unemprte + total_vmt +
    factor(name) + factor(year),
  data = data
)

# Estimate Event-Study Model for Occupant Fatality Rate
es_model_occ <- lm(
  occfat_per_100k ~ lead_6_plus + lead_5 + lead_4 + lead_3 + lead_2 +
    lag_0 + lag_1 + lag_2 + lag_3 + lag_4 + lag_5 + lag_6_plus +
    sbprim + sbsec + bac08 + mlda21 + pcinc + unemprte + total_vmt +
    factor(name) + factor(year),
  data = data
)

# ------------------------------------------------------------------------------
# 8. Event-Study Plot Generation
# ------------------------------------------------------------------------------

# Helper function to generate event-study plot data
build_es_plot_df <- function(es_model) {
  ct_es <- coeftest(es_model, vcov = vcovCL(es_model, cluster = ~name))
  
  # Extract estimates and standard errors
  estimates <- ct_es[event_vars, "Estimate"]
  ses <- ct_es[event_vars, "Std. Error"]
  
  # Insert omitted reference year (k = -1) with 0 estimate and 0 SE
  es_df <- data.frame(
    rel_year = c(-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6),
    coef = c(estimates[1:5], 0, estimates[6:12]),
    se = c(ses[1:5], 0, ses[6:12])
  )
  
  # Calculate 95% Confidence Intervals
  es_df$ci_lower <- es_df$coef - 1.96 * es_df$se
  es_df$ci_upper <- es_df$coef + 1.96 * es_df$se
  
  return(es_df)
}

es_overall_df <- build_es_plot_df(es_model)
es_occupant_df <- build_es_plot_df(es_model_occ)

# Plot for Overall Fatality Rate
p_overall <- ggplot(es_overall_df, aes(x = rel_year, y = coef)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray50", size = 0.5) +
  geom_vline(xintercept = -1, linetype = "dashed", color = "#b03a2e", size = 0.5) +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.15, color = "#1f4e79", size = 0.8) +
  geom_point(color = "#1f4e79", size = 3) +
  geom_line(color = "#1f4e79", linetype = "dotted") +
  scale_x_continuous(breaks = -6:6, labels = c("<= -6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5", ">= 6")) +
  labs(
    title = "Event-Study: Impact of 70 mph Speed Limit on Fatality Rate",
    subtitle = "Outcome: Traffic Fatalities per 100,000 population (95% CI, Clustered SE by State)",
    x = "Years Relative to lim70 Adoption",
    y = "Coefficient Estimate"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 12, color = "#1f4e79"),
    plot.subtitle = element_text(size = 9, color = "gray30"),
    axis.title = element_text(size = 10, face = "bold"),
    axis.text = element_text(size = 9),
    panel.grid.minor = element_blank()
  )

# Plot for Occupant Fatality Rate
p_occupant <- ggplot(es_occupant_df, aes(x = rel_year, y = coef)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray50", size = 0.5) +
  geom_vline(xintercept = -1, linetype = "dashed", color = "#b03a2e", size = 0.5) +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.15, color = "#1f4e79", size = 0.8) +
  geom_point(color = "#1f4e79", size = 3) +
  geom_line(color = "#1f4e79", linetype = "dotted") +
  scale_x_continuous(breaks = -6:6, labels = c("<= -6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5", ">= 6")) +
  labs(
    title = "Event-Study: Impact of 70 mph Speed Limit on Occupant Fatality Rate",
    subtitle = "Outcome: Vehicle Occupant Fatalities per 100,000 population (95% CI, Clustered SE by State)",
    x = "Years Relative to lim70 Adoption",
    y = "Coefficient Estimate"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 12, color = "#1f4e79"),
    plot.subtitle = element_text(size = 9, color = "gray30"),
    axis.title = element_text(size = 10, face = "bold"),
    axis.text = element_text(size = 9),
    panel.grid.minor = element_blank()
  )

# Save the plots
ggsave("graph_speed_limit_event_study.png", plot = p_overall, width = 7, height = 5, dpi = 300)
ggsave("graph_speed_limit_event_study_occupant.png", plot = p_occupant, width = 7, height = 5, dpi = 300)

# ------------------------------------------------------------------------------
# 9. Raw Trend Plots (Average Fatalities and Speed Limit Over Time)
# ------------------------------------------------------------------------------

# Calculate annual averages across all states
annual_avg <- aggregate(
  cbind(totfat, fatalities_per_100k, lim70) ~ year, 
  data = data, 
  FUN = mean, 
  na.rm = TRUE
)

# Plot raw trend of average fatalities per 100k over time
png("graph_average_fatalities_over_time.png", width = 2100, height = 1500, res = 300)
par(mar = c(5, 5, 4, 5))
plot(
  annual_avg$year, annual_avg$fatalities_per_100k, 
  type = "o", lwd = 2, col = "#b03a2e", pch = 16,
  main = "Average Fatality Rate and Speed Limit Adoption Over Time",
  xlab = "Year", ylab = "Fatalities per 100,000 population",
  ylim = c(min(annual_avg$fatalities_per_100k) - 1, max(annual_avg$fatalities_per_100k) + 1)
)
grid()
par(new = TRUE)
plot(
  annual_avg$year, annual_avg$lim70, 
  type = "l", lwd = 2, col = "#1f4e79", lty = 2,
  axes = FALSE, xlab = "", ylab = ""
)
axis(side = 4, at = seq(0, 1, by = 0.2))
mtext(side = 4, line = 3, "Share of States with Speed Limit >= 70 mph", col = "#1f4e79")
legend(
  "topright", 
  legend = c("Fatality Rate per 100k", "lim70 Share"), 
  col = c("#b03a2e", "#1f4e79"), 
  lty = c(1, 2), 
  lwd = 2, 
  pch = c(16, NA)
)
dev.off()

# ------------------------------------------------------------------------------
# 10. Export Clean Analysis Sample CSV
# ------------------------------------------------------------------------------

# Keep rows used in the main controlled TWFE model for transparency
clean_data <- data[complete.cases(data[, c(
  "fatalities_per_100k", "occfat_per_100k", "noccfat_per_100k", 
  "totfat", "totpop", "lim70", "sbprim", "sbsec", "bac08", 
  "mlda21", "pcinc", "unemprte", "total_vmt"
)]), ]

write.csv(clean_data, "speed_limit_fatalities_data.csv", row.names = FALSE)

# Confirm script completion
cat("Analysis script completed successfully. All outputs written to disk.\n")
cat("Sample size of clean analysis dataset:", nrow(clean_data), "\n")
