#setwd ('/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/HW1')
getwd ()

# Load the necessary packages
library (tidyverse)
library (readxl)
library (stargazer)
library (ggplot2)

data <- read.csv("HW1_wildfire_exposure.csv")

#Viewing Data
view(data) #views data set in new tab
head(data) #shows first 6 rows
str(data) #shows internal structure 
summary(data) #descriptive statistics

dim(data) 
# ==========================QUESTION 1=======================================
# There are 16 data frames or columns in this data set. Each corresponding to variables.

# ==========================QUESTION 2=======================================
# There 20990 observations

# ==========================QUESTION 3=======================================
# There are 16 variables

# ==========================QUESTION 4=======================================
#There are no missing data points. 
data[data == "."] <- NA #replaces any data that has a . with N/A
sum(is.na(data)) #give sum of na data 

# ==========================QUESTION 5=======================================
table(data$wildfire2yr5000)# There were 66 BG's that were at the center of the wildfires

# ==========================QUESTION 6=======================================
table(data$wildfire2yr5000) # There were 66 BGs that experienced Wildfires

table(
  `Center within 5km` = data$wildfire2yr5000,
  `Any wildfire (2yr)` = data$wildfire2yr
)
data$mindistkm <- data$mindist5000/1000
table(data$mindistkm)
summary(data$mindistkm) #descriptive statistics for minimum distance in km


mean_mindistkm <- mean(data$mindistkm, na.rm = TRUE)
var_mindistkm <- var(data$mindistkm, na.rm = TRUE)

mean_envbi <- mean(data$envbi, na.rm = TRUE)
var_envbi <- var(data$envbi, na.rm = TRUE)

cov_mindistkm_envbi <- cov(data$mindistkm, data$envbi, use = "complete.obs")

#Printing all variables
print(mean_mindistkm)
print(mean_envbi)
print(var_mindistkm)
print(var_envbi)
print(cov_mindistkm_envbi)

# ==========================3.3 Visualizing the Data=======================================
# GPS Color Palette (from brand guidelines)
gps_navy <- "#182B49"        # Primary navy blue for text and borders
gps_gold <- "#C69214"        # Primary gold for accent elements
gps_gold_50 <- "#E3C98A"     # 50% tint gold for softer accents
gps_blue_50 <- "#80B1CD"     # 50% tint blue for histogram fills
gps_sand <- "#F5F0E6"        # Sand neutral for backgrounds

# Calculate bin width for proper density scaling
envbi_range <- max(data$envbi, na.rm = TRUE) - min(data$envbi, na.rm = TRUE)  # Find range of data
envbi_binwidth <- envbi_range / 50  # Divide by number of bins to get width of each bin

# EBI histogram with GPS styling
plot_envbi <- ggplot(data, aes(x = envbi)) +  # Initialize ggplot with data and x-axis aesthetic
  geom_histogram(  # Add histogram layer
    aes(y = after_stat(count)),  # Use count (frequency) for y-axis; after_stat() computes this from data
    bins = 50,  # Divide data into 50 bins
    fill = gps_blue_50,  # Fill bars with GPS blue 50% tint
    alpha = 0.8,  # Set transparency to 0.8 (80% opaque) for subtle appearance
    color = gps_navy,  # Outline each bar with GPS navy color
    linewidth = 0.3  # Set border thickness to 0.3
  ) +
  geom_density(  # Add density curve layer
    aes(y = after_stat(density * nrow(data) * envbi_binwidth)),  # Scale density to match histogram count scale
    color = gps_gold,  # Draw density line in GPS gold color
    linewidth = 1.2  # Make density line thicker (1.2) for visibility
  ) +
  scale_x_continuous(  # Customize x-axis scale
    breaks = seq(0.2, 1.0, by = 0.05)  # Create tick marks every 0.05 units from 0.2 to 1.0
  ) +
  scale_y_continuous(  # Customize y-axis scale
    breaks = seq(0, 900, by = 100)  # Create tick marks every 100 units from 0 to 900
  ) +
  labs(  # Add labels to the plot
    title = "Distribution of EBI",  # Main title at top of plot
    x = "Environmental Ballot Index",  # X-axis label
    y = "Frequency"  # Y-axis label
  ) +
  theme_minimal(base_size = 14) +  # Apply minimal theme with 14pt base font size
  theme(  # Customize theme elements
    panel.background = element_rect(fill = "white"),  # Set inner plot area background to white
    plot.background = element_rect(fill = gps_sand),  # Set outer plot background to GPS sand color
    plot.title = element_text(color = gps_navy, face = "bold"),  # Make title GPS navy and bold
    axis.title = element_text(color = gps_navy),  # Make axis labels GPS navy
    axis.text = element_text(color = gps_navy),  # Make axis tick labels GPS navy
    panel.grid.major = element_line(color = "#DBD8D4", linewidth = 0.3),  # Add subtle major gridlines
    panel.grid.minor = element_blank()  # Remove minor gridlines for cleaner look
  )

print(plot_envbi)  # Display plot in RStudio Plots pane
ggsave("distribution_envbi.png", plot = plot_envbi, width = 8, height = 6, bg = "white")  # Save as PNG file (8x6 inches, white background)

# Minimum Distance histogram with GPS styling
mindist_range <- max(data$mindistkm, na.rm = TRUE) - min(data$mindistkm, na.rm = TRUE)  # Find range of distance data
mindist_binwidth <- mindist_range / 50  # Calculate bin width for 50 bins

plot_mindistkm <- ggplot(data, aes(x = mindistkm)) +  # Initialize ggplot with distance data on x-axis
  geom_histogram(  # Add histogram layer
    aes(y = after_stat(count)),  # Use count (frequency) for y-axis
    bins = 50,  # Divide data into 50 bins
    fill = gps_blue_50,  # Fill bars with GPS blue 50% tint
    alpha = 0.8,  # Set transparency to 80% for softer appearance
    color = gps_navy,  # Outline bars with GPS navy
    linewidth = 0.3  # Set thin border (0.3) for bars
  ) +
  geom_density(  # Add density curve overlay
    aes(y = after_stat(density * nrow(data) * mindist_binwidth)),  # Scale density curve to match histogram height
    color = gps_gold,  # Use GPS gold for density line
    linewidth = 1.2  # Make line prominent with 1.2 thickness
  ) +
  scale_x_continuous(  # Customize x-axis scale
    breaks = seq(0, 250, by = 25)  # Create tick marks every 25 km from 0 to 250
  ) +
  scale_y_continuous(  # Customize y-axis scale
    breaks = seq(0, 1800, by = 200)  # Create tick marks every 200 units from 0 to 1800
  ) +
  labs(  # Add plot labels
    title = "Distribution of Minimum Distance to Wildfire Epicenter",  # Descriptive title
    x = "Distance (km)",  # X-axis shows distance in kilometers
    y = "Frequency"  # Y-axis shows count of observations
  ) +
  theme_minimal(base_size = 14) +  # Start with clean minimal theme, 14pt font
  theme(  # Customize specific theme elements
    panel.background = element_rect(fill = "white"),  # White background for data area
    plot.background = element_rect(fill = gps_sand),  # GPS sand for surrounding area
    plot.title = element_text(color = gps_navy, face = "bold"),  # Bold navy title
    axis.title = element_text(color = gps_navy),  # Navy axis labels
    axis.text = element_text(color = gps_navy),  # Navy tick mark labels
    panel.grid.major = element_line(color = "#DBD8D4", linewidth = 0.3),  # Light gray major gridlines
    panel.grid.minor = element_blank()  # No minor gridlines
  )

print(plot_mindistkm)  # Display plot in Plots pane
ggsave("distribution_mindistkm.png", plot = plot_mindistkm, width = 8, height = 6, bg = "white")  # Save as 8x6 inch PNG with white background

# Regression line 
plot_lm_mindistkm_envbi <- ggplot(data, aes(x = mindistkm, y = envbi)) +
  geom_point(alpha = 0.2, size = 1) +
  geom_smooth(method = "lm", se = TRUE, color = "red") +
  labs(
    title = "EBI vs. Distance to Wildfire",
    x = "Distance to Wildfire (km)",
    y = "Environmental Ballot Index"
  ) +
  scale_y_continuous(limits = c(0, 1)) +
  theme_minimal()

print(plot_lm_mindistkm_envbi) # places graph into plots
ggsave("scatter_regression_envbi_mindistk.png", plot = plot_lm_mindistkm_envbi, width = 8, height = 6)

# ==========================3.4 Regression Analysis=======================================
model <- lm(envbi ~ mindistkm, data = data) # y=envbi x=mindistkm
summary(model) #prints into console

#Using Stargazer to get nice table
stargazer(
  model,
  type = "html",
  title = "OLS Regression: Environmental Ballot Index",
  dep.var.labels = "Environmental Ballot Index (EBI)",
  covariate.labels = "Distance to Wildfire (km)",
  out = "regression_envbi_mindistkm.html"
)
#=========================Question 8 Manual Calculation========================
b1_manual <- cov_mindistkm_envbi / var_mindistkm #calculates b1 by dividing covariance of x&y by variance of x
b0_manual <- mean_envbi - b1_manual * mean_mindistkm #calculates b0

#Prints calculations 
print(b1_manual)
print(b0_manual)
model_summary <- summary(model)
b0_lm <- coef(model)[1]  # Intercept
b1_lm <- coef(model)[2]  # Slope
se_b0 <- model_summary$coefficients[1, 2]
se_b1 <- model_summary$coefficients[2, 2]
p_b0 <- model_summary$coefficients[1, 4]
p_b1 <- model_summary$coefficients[2, 4]
r_squared <- model_summary$r.squared

# Create comparison table
comparison_table <- data.frame(
  Coefficient = c("Intercept (b0)", "Slope (b1)"),
  Manual_Calculation = c(b0_manual, b1_manual),
  lm_Function = c(b0_lm, b1_lm),
  Difference = c(b0_manual - b0_lm, b1_manual - b1_lm)
)

# Round to 6 decimal places for clarity
comparison_table[, 2:4] <- round(comparison_table[, 2:4], 6)

# Print the table
print(comparison_table)

#Saves as Html for word document
stargazer(comparison_table,
          type = "html",
          summary = FALSE,
          title = "Table: Comparison of Manual OLS Calculation vs lm() Function",
          rownames = FALSE,
          out = "coefficient_comparison.html")

#===============Is there a 3 party variable?============================
# Estimate both models
model <- lm(envbi ~ mindistkm, data = data)
model_envbi_mindistkm_votesharedem <- lm(envbi ~ mindistkm + voteshare_dem, data = data)

# Create comparison table with stargazer
stargazer(
  model, model_envbi_mindistkm_votesharedem,
  type = "html",
  title = "OLS Regression: Environmental Ballot Index",
  dep.var.labels = "Environmental Ballot Index (EBI)",
  covariate.labels = c("Distance to Wildfire (km)", "Democratic Vote Share"),
  column.labels = c("Bivariate", "Multivariate"),
  model.numbers = FALSE,
  out = "regression_comparison_envbi.html"
)
