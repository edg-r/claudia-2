# Set working directory
setwd('/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/R Studio/2 Plots and Regression')
getwd()

# Load the necessary packages
library(tidyverse)
library(readxl)
library(stargazer)
library(ggplot2)

# Load the datasets
corruption_data <- read_csv("corruption_index.csv")
diplomatic_data <- read_excel("diplomatic_parking_tickets.xlsx")

# View the structure of each dataset
str(corruption_data)
str(diplomatic_data)

# Merge the datasets by the common variable "country_code"
merged_data <- merge(corruption_data, diplomatic_data, by = "country_code")

# View the first few rows of the merged dataset
head(merged_data)



# Scatter plot of vpd_9702 against ci1998 with country_code labels
ggplot(data = merged_data, aes(x = ci1998, y = vpd_9702, label = country_code)) +
  geom_point() +
  geom_text(vjust = -0.5, size = 3) +
  labs(title = "Total Parking Violations (1997-2002) vs Corruption Index (1998)",
       x = "Corruption Index 1998",
       y = "Total Parking Violations") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

# Create a new variable: parking violations per diplomat
merged_data <- merged_data %>%
  mutate(vpd_per_diplomat = vpd_9702 / diplomat_count98)

# Scatter plot of vpd_per_diplomat against ci1998 with country_code labels
ggplot(data = merged_data, aes(x = ci1998, y = vpd_per_diplomat, label = country_code)) +
  geom_point() +
  geom_text(vjust = -0.5, size = 3) +
  labs(title = "Parking Violations per Diplomat vs Corruption Index (1998)",
       x = "Corruption Index 1998",
       y = "Parking Violations per Diplomat") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))


# Create a new variable: log(1 + parking violations per diplomat)
merged_data <- merged_data %>%
  mutate(log_vpd_per_diplomat = log(1 + vpd_per_diplomat))

# Scatter plot of log(1 + vpd_per_diplomat) against ci1998 with country_code labels
ggplot(data = merged_data, aes(x = ci1998, y = log_vpd_per_diplomat, label = country_code)) +
  geom_point() +
  geom_text(vjust = -0.5, size = 3) +
  labs(title = "Log(1 + Parking Violations per Diplomat) vs Corruption Index (1998)",
       x = "Corruption Index 1998",
       y = "Log(1 + Parking Violations per Diplomat)") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))


# Estimate the model using lm()
model <- lm(log_vpd_per_diplomat ~ ci1998, data = merged_data) #lm(y variable(output) ~ x var (explanatory variable) from merged data)
summary(model) #prints into console

# Save regression results to a text file
stargazer(
  model, 
  type = "text", 
  title = "Bivariate Regression Results: Corruption Index Predicting Log(Parking Violations per Diplomat)",
  dep.var.labels = "Dependent Variable: Log(1 + Parking Violations per Diplomat)",
  covariate.labels = c("Corruption Index (1998)", "Intercept"),
  out = "regression_results.txt"
)


# Save scatter plot with regression line and 95% confidence interval as a figure
ggplot(data = merged_data, aes(x = ci1998, y = log_vpd_per_diplomat)) +
  geom_point(alpha = 0.7) +
  geom_smooth(method = "lm", se = TRUE, color = "blue") +
  labs(title = "Regression of Log(Parking Violations per Diplomat) on Corruption Index",
       x = "Corruption Index 1998",
       y = "Log(1 + Parking Violations per Diplomat)") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))
  ggsave("scatter_plot_regression_fit.png")


# Calculate residuals and fitted values
residuals <- residuals(model)
fitted_values <- fitted(model)

# Scatter plot of residuals vs. fitted values
plot(fitted_values, residuals,
     main = "Residuals vs. Fitted Values",
     xlab = "Fitted Values",
     ylab = "Residuals",
     pch = 19, col = "darkgray")
abline(h = 0, col = "red", lty = 2)



# Load the negative relationship dataset
negative_data <- read.csv("negative_relationship_data.csv")

# View the structure of the data
str(negative_data)

# Plot the data to verify the relationship
library(ggplot2)
ggplot(data = negative_data, aes(x = ci1998, y = log_vpd_per_diplomat, label = country_code)) +
  geom_point(alpha = 0.7, color = "blue") +
  geom_text(vjust = -0.5, size = 3, color = "darkgray") +
  geom_smooth(method = "lm", se = TRUE, color = "red") +
  labs(title = "Negative Relationship: Sample Selection Bias Example",
       x = "Corruption Index (1998)",
       y = "Log(1 + Parking Violations per Diplomat)") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))