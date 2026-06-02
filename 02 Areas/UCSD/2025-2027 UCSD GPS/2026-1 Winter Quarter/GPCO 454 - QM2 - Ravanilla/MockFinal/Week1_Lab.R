# Set working directory
setwd ('/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/R Studio/Week 1')
getwd()

# Load the necessary packages
library(tidyverse)
library(readxl)
library(stargazer)

# Load the dataset
data <- read_excel("gpa_and_qm2_confidence.xlsx")

# View data
View(data)

# Preview the dataset
head(data)
str(data)
summary(data)

# Rename columns
colnames(data) <- c("Student", "GPA", "Confidence")

# Replace "." with NA
data[data == "."] <- NA
sum(is.na(data))

# Convert specific columns to numeric (one by one)
data$GPA <- as.numeric(data$GPA)  
data$Confidence <- as.numeric(data$Confidence)

# Calculate descriptive statistics
mean_gpa <- mean(data$GPA, na.rm = TRUE)
mean_confidence <- mean(data$Confidence, na.rm = TRUE)
var_gpa <- var(data$GPA, na.rm = TRUE)
var_confidence <- var(data$Confidence, na.rm = TRUE)
cov_gpa_confidence <- cov(data$GPA, data$Confidence, use = "complete.obs")

# View the results
print(mean_gpa)
print(mean_confidence)
print(var_gpa)
print(var_confidence)
print(cov_gpa_confidence)

# Visualize the data
# Distribution of GPAs with Frequency and Scaled Kernel Density
plot_gpa <- ggplot(data, aes(x = GPA)) +
  geom_histogram(
    aes(y = ..count..), 
    bins = 10, 
    fill = "blue", 
    alpha = 0.5, 
    color = "black"
  ) +
  geom_density(
    aes(y = ..density.. * nrow(data) * (4.0 / 10)), 
    color = "red", 
    size = 1
  ) +
  labs(
    title = "Distribution of GPA",
    x = "GPA",
    y = "Frequency"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    panel.background = element_rect(fill = "white"),
    plot.background = element_rect(fill = "white")
  )
ggsave("distribution_gpa.png", plot = plot_gpa, width = 8, height = 6)

# Distribution of Confidence with Frequency and Scaled Kernel Density
plot_confidence <- ggplot(data, aes(x = Confidence)) +
  geom_histogram(
    aes(y = ..count..), 
    bins = 10, 
    fill = "blue", 
    alpha = 0.5, 
    color = "black"
  ) +
  geom_density(
    aes(y = ..density.. * nrow(data) * (100.0 / 10)), 
    color = "red", 
    size = 1
  ) +
  labs(
    title = "Distribution of Confidence",
    x = "Confidence",
    y = "Frequency"
  )
ggsave("distribution_confidence.png", plot = plot_confidence, width = 8, height = 6)

# Scatter Plot of GPA vs. Confidence
plot_scatter <- ggplot(data, aes(x = GPA, y = Confidence)) +
  geom_point(shape = 4, color = "blue", size = 2, alpha = 0.7) +
  labs(
    title = "Scatter Plot of GPA vs. Confidence",
    x = "GPA",
    y = "Confidence"
  ) +
  scale_x_continuous(
    breaks = seq(0, 5.0, by = 0.5), 
    limits = c(0, 5.0)
  ) +
  scale_y_continuous(
    breaks = seq(-10, 100, by = 10),  
    limits = c(-10, 100)
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    axis.title = element_text(face = "bold")
  )
ggsave("scatter_gpa_confidence.png", plot = plot_scatter, width = 8, height = 6)

# Estimate the bivariate regression model and report results
model <- lm(Confidence ~ GPA, data = data)
summary(model)
stargazer(
  model, 
  type = "text", 
  title = "Bivariate Regression Results: GPA Predicting Confidence",
  dep.var.labels = "Dependent Variable: Confidence",
  covariate.labels = c("GPA", "Intercept"),
  out = "regression_results.txt"
)

# Manual calculation of regression coefficients
# Use pre-calculated variance and covariance
b1 <- cov_gpa_confidence / var_gpa
b0 <- mean_confidence - b1 * mean_gpa

# Display manual coefficients
cat("Manual Calculation - Slope (b1):", b1, "\n")
cat("Manual Calculation - Intercept (b0):", b0, "\n")

# Compare manual coefficients with lm() coefficients
cat("lm() Coefficients:\n")
print(coef(model))

# Scatter Plot of GPA vs. Confidence with the regression line
plot_scatter_with_fit <- ggplot(data, aes(x = GPA, y = Confidence)) +
  geom_point(shape = 4, color = "blue", size = 2, alpha = 0.7) +
  geom_smooth(method = "lm", color = "red", se = TRUE, size = 1) +
  labs(
    title = "Scatter Plot of GPA vs. Confidence",
    x = "GPA",
    y = "Confidence"
  ) +
  scale_x_continuous(
    breaks = seq(0, 5.0, by = 0.5), 
    limits = c(0, 5.0)
  ) +
  scale_y_continuous(
    breaks = seq(-10, 100, by = 10),  
    limits = c(-10, 100)
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    axis.title = element_text(face = "bold"),
    panel.background = element_rect(fill = "white"),
    plot.background = element_rect(fill = "white")
  )
ggsave("scatter_gpa_confidence_with_fit.png", plot = plot_scatter_with_fit, width = 8, height = 6)