# Week 7 Lab Script: Handling Outliers
# GPCO 454 - Quantitative Methods II (QM2)
# Date: February 20, 2026

# ---------------------------
# A. Preliminaries
# ---------------------------

rm(list = ls()) # Clear the workspace)

# 1. Set your working directory and load the necessary packages in your R script.

setwd("~/Desktop/QM2 R Materials/Week 7") # <- this should be changed to your directory and commented out!
getwd() # Check the working directory

#Install the necessary packages
#install.packages("tidyverse")
#install.packages("readxl")
#install.packages("stargazer")
#install.packages("ggplot2")

library(tidyverse)
library(readxl)
library(stargazer)
library(ggplot2)

# 2. Load the dataset into R.

diplomatic_data <- read.csv("diplomatic_data.csv")

# Inspect the dataset structure
head(diplomatic_data)
summary(diplomatic_data)

# =============================================================================
# B. Identifying Outliers Using Visual Method
# =============================================================================

# 1. Histogram of vpd_per_diplomat
ggplot(diplomatic_data, aes(x = vpd_per_diplomat)) +
  geom_histogram(binwidth = 2, fill = "skyblue", color = "black") +
  labs(title = "Histogram of Parking Violations per Diplomat",
       x = "Violations per Diplomat (vpd_per_diplomat)",
       y = "Frequency") +
  theme_minimal()

# 2. Boxplot of vpd_per_diplomat
ggplot(diplomatic_data, aes(x = "All Countries", y = vpd_per_diplomat)) +
  geom_boxplot(fill = "lightcoral", outlier.color = "red", outlier.shape = 16) +
  scale_y_continuous(limits = c(-10, 150)) +  # Expand the range
  labs(title = "Boxplot of Parking Violations per Diplomat",
       x = "All Countries",
       y = "Violations per Diplomat (vpd_per_diplomat)") +
  theme_minimal()

# 3. Scatter plot of vpd_per_diplomat vs. ci1998
ggplot(diplomatic_data, aes(x = ci1998, y = vpd_per_diplomat)) +
  geom_point(color = "darkgreen", alpha = 0.7) +
  geom_smooth(method = "lm", color = "red", se = FALSE) +
  labs(title = "Scatter Plot of Parking Violations per Diplomat vs. Corruption Index (1998)",
       x = "Corruption Index (ci1998)",
       y = "Violations per Diplomat (vpd_per_diplomat)") +
  theme_minimal()


# =============================================================================
# C. Identifying Outliers Using Statistical Methods
# =============================================================================

# Fit a linear model: Violations per diplomat explained by corruption index (ci1998)
mod <- lm(vpd_per_diplomat ~ ci1998, data = diplomatic_data)

# 1. Studentized Residuals
diplomatic_data$studentized_residuals <- rstudent(mod)

# Identify potential outliers based on the rule: abs(residual) > 2
outliers_residuals <- diplomatic_data %>%
  filter(abs(studentized_residuals) > 2)

cat("\nObservations with Studentized Residuals > 2:\n")
print(outliers_residuals[, c("country_name.x", "vpd_per_diplomat", "studentized_residuals")])

# -----------------------------------------------------------------------------

# 2. Leverage
diplomatic_data$leverage <- hatvalues(mod)

# Rule of thumb: Leverage > 2(k+2)/n
k <- length(coef(mod)) - 1  # Number of predictors
n <- nrow(diplomatic_data)
leverage_threshold <- 2 * (k + 2) / n

outliers_leverage <- diplomatic_data %>%
  filter(leverage > leverage_threshold)

cat("\nObservations with High Leverage (> 2(k+2)/n):\n")
print(outliers_leverage[, c("country_name.x", "vpd_per_diplomat", "leverage")])

# -----------------------------------------------------------------------------

# 3. Cook's Distance
diplomatic_data$cooks_distance <- cooks.distance(mod)

# Rule of thumb: Cook's Distance > 4/n
cooks_threshold <- 4 / n

outliers_cooks <- diplomatic_data %>%
  filter(cooks_distance > cooks_threshold)

cat("\nObservations with High Cook's Distance (> 4/n):\n")
print(outliers_cooks[, c("country_name.x", "vpd_per_diplomat", "cooks_distance")])

# -----------------------------------------------------------------------------

# 4. Difference in Fitted Values (DFFITS)
diplomatic_data$dffits <- dffits(mod)

# Rule of thumb: |DFFITS| > 2 * sqrt(k/n)
dffits_threshold <- 2 * sqrt(k / n)

outliers_dffits <- diplomatic_data %>%
  filter(abs(dffits) > dffits_threshold)

cat("\nObservations with High DFFITS (> 2√(k/n)):\n")
print(outliers_dffits[, c("country_name.x", "vpd_per_diplomat", "dffits")])

# -----------------------------------------------------------------------------

# 5. Change in Coefficients (DFBETAS)
dfbetas_values <- dfbetas(mod)

# Convert to a data frame for easier interpretation
dfbetas_df <- as.data.frame(dfbetas_values)
diplomatic_data$dfbetas_ci1998 <- dfbetas_df$ci1998

# Rule of thumb: |DFBETAS| > 2 / sqrt(n)
dfbetas_threshold <- 2 / sqrt(n)

outliers_dfbetas <- diplomatic_data %>%
  filter(abs(dfbetas_ci1998) > dfbetas_threshold)

cat("\nObservations with High DFBETAS (> 2/sqrt(n)):\n")
print(outliers_dfbetas[, c("country_name.x", "vpd_per_diplomat", "dfbetas_ci1998")])

# -----------------------------------------------------------------------------

# 6. Summary of Influence Measures
cat("\n=== Influence Measures Summary ===\n")
influence_summary <- influence.measures(mod)
print(head(influence_summary))

# -----------------------------------------------------------------------------

# 7. Visualizing Influential Points
par(mfrow = c(2, 2))

# Studentized Residuals Plot
plot(diplomatic_data$ci1998, diplomatic_data$studentized_residuals,
     main = "Studentized Residuals",
     xlab = "Corruption Index (ci1998)",
     ylab = "Studentized Residuals",
     pch = 16, col = ifelse(abs(diplomatic_data$studentized_residuals) > 2, "red", "blue"))
abline(h = c(-2, 2), col = "red", lty = 2)

# Leverage Plot
plot(diplomatic_data$ci1998, diplomatic_data$leverage,
     main = "Leverage Values",
     xlab = "Corruption Index (ci1998)",
     ylab = "Leverage",
     pch = 16, col = ifelse(diplomatic_data$leverage > leverage_threshold, "red", "blue"))
abline(h = leverage_threshold, col = "red", lty = 2)

# Cook's Distance Plot
plot(diplomatic_data$ci1998, diplomatic_data$cooks_distance,
     main = "Cook's Distance",
     xlab = "Corruption Index (ci1998)",
     ylab = "Cook's Distance",
     pch = 16, col = ifelse(diplomatic_data$cooks_distance > cooks_threshold, "red", "blue"))
abline(h = cooks_threshold, col = "red", lty = 2)

# DFFITS Plot
plot(diplomatic_data$ci1998, diplomatic_data$dffits,
     main = "DFFITS",
     xlab = "Corruption Index (ci1998)",
     ylab = "DFFITS",
     pch = 16, col = ifelse(abs(diplomatic_data$dffits) > dffits_threshold, "red", "blue"))
abline(h = c(-dffits_threshold, dffits_threshold), col = "red", lty = 2)

# Reset plot layout
par(mfrow = c(1, 1))

# -----------------------------------------------------------------------------

# Key Takeaways
cat("\n=== Key Takeaways ===\n")
cat("- Observations flagged by multiple methods are likely influential.\n")
cat("- Consider removing extreme points and refitting the model.\n")
cat("- Examine whether removing outliers significantly changes coefficients.\n")


# =============================================================================
# D. Approaches to Handling Outliers
# =============================================================================

# 1. Original Model (Baseline)
mod_original <- lm(vpd_per_diplomat ~ ci1998, data = diplomatic_data)

# -----------------------------------------------------------------------------
# 2. Trimming: Remove extreme outliers based on Cook's Distance
# -----------------------------------------------------------------------------

# Threshold for Cook's Distance
cooks_threshold <- 4 / nrow(diplomatic_data)

# Identify and remove influential observations
trimmed_data <- diplomatic_data %>%
  filter(cooks.distance(mod_original) <= cooks_threshold)

# Fit the trimmed model
mod_trimmed <- lm(vpd_per_diplomat ~ ci1998, data = trimmed_data)

# -----------------------------------------------------------------------------
# 3. Winsorizing: Cap extreme values at the 5th and 95th percentiles
# -----------------------------------------------------------------------------

# Winsorize the outcome variable
winsorize <- function(x, prob = 0.05) {
  lower <- quantile(x, prob)
  upper <- quantile(x, 1 - prob)
  x[x < lower] <- lower
  x[x > upper] <- upper
  return(x)
}

# Apply winsorization
diplomatic_data$winsorized_vpd <- winsorize(diplomatic_data$vpd_per_diplomat)

# Fit the winsorized model
mod_winsorized <- lm(winsorized_vpd ~ ci1998, data = diplomatic_data)

# -----------------------------------------------------------------------------
# 4. Log Transformation of the Outcome Variable
# -----------------------------------------------------------------------------

# Log-transform the outcome variable (adding 1 to avoid log(0))
diplomatic_data$log_vpd <- log1p(diplomatic_data$vpd_per_diplomat)

# Fit the log-transformed model
mod_log <- lm(log_vpd ~ ci1998, data = diplomatic_data)

# =============================================================================
# 5. Regression Comparison: Side-by-Side Output
# =============================================================================

# Load the stargazer package for side-by-side comparison
library(stargazer)

# Display regression results side by side
stargazer(mod_original, mod_trimmed, mod_winsorized, mod_log,
          type = "text",
          title = "Comparison of Approaches to Handling Outliers",
          column.labels = c("Original", "Trimmed", "Winsorized", "Log Transformed"),
          dep.var.labels = "Parking Violations per Diplomat",
          covariate.labels = c("Corruption Index (ci1998)", "Intercept"),
          digits = 3,
          align = TRUE,
          star.cutoffs = c(0.05, 0.01, 0.001))

# =============================================================================
# 6. Visualizing Model Fit for Each Approach
# =============================================================================

par(mfrow = c(2, 2))

# Original Model
plot(diplomatic_data$ci1998, diplomatic_data$vpd_per_diplomat,
     main = "Original Model",
     xlab = "Corruption Index (ci1998)",
     ylab = "Violations per Diplomat",
     pch = 16, col = "blue")
abline(mod_original, col = "red", lwd = 2)

# Trimmed Model
plot(trimmed_data$ci1998, trimmed_data$vpd_per_diplomat,
     main = "Trimmed Model (Cook's Distance)",
     xlab = "Corruption Index (ci1998)",
     ylab = "Violations per Diplomat",
     pch = 16, col = "darkgreen")
abline(mod_trimmed, col = "red", lwd = 2)

# Winsorized Model
plot(diplomatic_data$ci1998, diplomatic_data$winsorized_vpd,
     main = "Winsorized Model (5th/95th Percentile)",
     xlab = "Corruption Index (ci1998)",
     ylab = "Violations per Diplomat (Winsorized)",
     pch = 16, col = "orange")
abline(mod_winsorized, col = "red", lwd = 2)

# Log-Transformed Model
plot(diplomatic_data$ci1998, diplomatic_data$log_vpd,
     main = "Log-Transformed Model",
     xlab = "Corruption Index (ci1998)",
     ylab = "Log Violations per Diplomat",
     pch = 16, col = "purple")
abline(mod_log, col = "red", lwd = 2)

# Reset plot layout
par(mfrow = c(1, 1))

