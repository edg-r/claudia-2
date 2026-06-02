# Week 8 Lab Script: Interactions in Regressions
# GPCO 454 - Quantitative Methods II (QM2)
# Date: February 27, 2026

# ---------------------------
# Section A - Preliminaries
# ---------------------------

# 1. Set your working directory and load the necessary packages in your R script.

setwd("~/Desktop/QM2 R Materials/Week 8") # <- this should be changed to your directory and commented out!

# Install the necessary packages if not already installed
# install.packages("tidyverse")
# install.packages("readr")
# install.packages("stargazer")
# install.packages("ggplot2")
# install.packages("ggeffects")

library(tidyverse)
library(readr)
library(stargazer)
library(ggplot2)
library(ggeffects)

# 2. Load the dataset into R
# read.table is used to read tab-delimited files, and the encoding is set to "ISO-8859-1" to handle special characters in the dataset.
# sep="\t" specifies that the file is tab-delimited, and header=TRUE indicates that the first row contains column names.
justice_data <- read.table("justice_results.tab", 
                           header = TRUE, 
                           sep = "\t", 
                           encoding = "ISO-8859-1")

# how to save this into excel
# write.csv(justice_data, "justice_results.csv", row.names = FALSE)

# 3. Explore the dataset
# Display the structure of the dataset
str(justice_data)

# 4. Summarize the key variables
summary(justice_data)

# 5. Count unique observations in the 'docket' variable
unique_cases <- justice_data %>% 
  summarize(unique_dockets = n_distinct(docket))
print(unique_cases)

# 6. Check for missing values
missing_values <- colSums(is.na(justice_data))
print(missing_values)


# ---------------------------
# Section B - Creating New Categorical Variables
# ---------------------------

# 1. Create a binary variable: high_pitch_variation
# This variable indicates whether the absolute difference between petitioner and respondent pitch 
# is greater than the median value, capturing cases where pitch contrast was unusually high.

# petitioner_pitch - respondent_pitch measures how much the petitioner's pitch differs from the respondent's pitch.
# add an abs so is distnace, and distnace is always positive. How much the pitch differs in absolute value 
# Then will define a large variation if the distance value is above the median X > median(X)
# to make this into a dummy we use ifelse. Ifelse(our condition as above, 1, 0)
# and we add na.rm= TRUE to deal with missing values

justice_data <- justice_data %>%
  mutate(high_pitch_variation = ifelse(abs(petitioner_pitch - respondent_pitch) > 
                                         median(abs(petitioner_pitch - respondent_pitch), na.rm = TRUE), 1, 0))

# we new variable, so what we do?
 # - check that variable was created by checking the last variable in the dataframe 
 # - as we created a dummy, make sure that has only 1 anrd 0 
 # - Check that the 1 and 0 actually correspont to the condition you intended

## just to check lets:
# 1. create the difference as variable 
# 2. Create the median difference as variable so we can visualy check the condition
justice_data <- justice_data %>%
  mutate(differenc_pitch = abs(petitioner_pitch - respondent_pitch),
         median_difference = median(abs(petitioner_pitch - respondent_pitch), na.rm = TRUE),
         high_pitch_variation = ifelse(abs(petitioner_pitch - respondent_pitch) > 
                                         median(abs(petitioner_pitch - respondent_pitch), na.rm = TRUE), 1, 0))
# great it works! 

# 2. Create a categorical variable: decade_category
# We classify cases into decades based on the term (court session year).

# we are going to create a categorical variable
  # Whats a categorical variable is variable that takes values from a set of categories.
  # eg. 60-70 B-, 70-80 B, 80-90 B+, 90-00 A-, 00-10 A, 10-20 A+
# how we do this, with case_when

# eg with letter grades:
# mutate(letter_grade = case_when( grade < 60 ~ "F",
#            grade >= 60 & grade < 70 ~ "D",
#            grade >= 70 & grade < 80 ~ "C",
#            grade >= 80 & grade < 90 ~ "B",
#            grade >= 90 ~ "A"))

justice_data <- justice_data %>%
  mutate(decade_category = case_when(
    term < 1960 ~ "1950s and earlier",
    term >= 1960 & term < 1970 ~ "1960s",
    term >= 1970 & term < 1980 ~ "1970s",
    term >= 1980 & term < 1990 ~ "1980s",
    term >= 1990 & term < 2000 ~ "1990s",
    term >= 2000 & term < 2010 ~ "2000s",
    term >= 2010 ~ "2010s"
  ))

# so far this new variable is a character variable, we want to make it a factor variable so that R treats it as categorical in our regression models.

# type of variables:
# numeric. -> as.numeric() to convert to numeric
# integer -> as.integer() to convert to integer
# character -> as.character() to convert to character
# factor -> as.factor() to convert to factor

# 3. Convert the categorical variable to a factor
justice_data$decade_category <- factor(justice_data$decade_category, 
                                       levels = c("1950s and earlier", "1960s", "1970s", 
                                                  "1980s", "1990s", "2000s", "2010s"))


# 4. Verify the new variables

#table creates a frequency table
# a frequency table is a table with the unique values 
  #of a variable and the number of times each value appears 
  #in the dataset
table(justice_data$high_pitch_variation)
table(justice_data$decade_category)

# ---------------------------
# Section C - Regression Analyses
# ---------------------------

# Let's imagine your interested on aswering the question: 
# Does speach characteristics relate to decision making in the Supreme Court?

# 1. Estimate First Regression Model (Baseline Model)
m_c_1 <- lm(petitioner_vote ~ high_pitch_variation + decade_category, data = justice_data)

# outcome: binary if the justice votes for the petitioner or not
# predictor: high_pitch_variable: binary if the diffence in pitch is above the median difference
# control: decade

# 2. Addressing Justice-Specific Effects (Fixed Effects)
m_c_2 <- lm(petitioner_vote ~ high_pitch_variation + decade_category + justiceName, data = justice_data)


# 3. Adding Term-Specific Indicators
m_c_3 <- lm(petitioner_vote ~ high_pitch_variation + decade_category + justiceName + as.factor(term), data = justice_data)

# Combine all three models into one regression table and save as a single text file
stargazer(m_c_1, m_c_2, m_c_3, 
          type = "text", 
          title = "Regression Results - Combined Models",
          out = "Lab8_CombinedModels.txt",
          dep.var.labels = "Probability of Voting for Petitioner",
          star.cutoffs = c(0.05, 0.01, 0.001),
          notes = "Standard errors in parentheses. * p<0.05, ** p<0.01, *** p<0.001")

## so what's going on:

# what's a fixed effect: Is equivalent to add a set dummy variables to the regression.

# What does a dummy do? income ~ education + female + as.factor(region)
# this as.factor(region) is the same as adding a dummy for each state.
# Effectively this accounts for the time invariant characteristics of each state.

# model 2 adds justice fixed effects: Control for the time invariant
# charactetistics of each justice. (Ideology (stable), backgroung, etc.)

# model 3 adds term (year) fixed effects: Control for shock/trends 
#common to all observation in a given year (eg. economic crisis, war, etc.)

# quiz code: hw3


# 1. Interaction Between Pitch Variation and Decade Category
# Examining whether the effect of pitch variation depends on the decade.
m_c_4 <- lm(petitioner_vote ~ high_pitch_variation * decade_category, data = justice_data)

# ---------------------------
# Version 1: X-axis = Decade Category, Interaction with High Pitch Variation (New)
# ---------------------------
ggpredict(m_c_4, terms = c("decade_category", "high_pitch_variation"))

fig_c_1 <- ggpredict(m_c_4, terms = c("decade_category", "high_pitch_variation"))

ggplot(fig_c_1, aes(x = x, y = predicted, color = group)) +
  geom_point(position = position_dodge(width = 0.3), size = 3) +  # Points for means
  geom_errorbar(aes(ymin = conf.low, ymax = conf.high), 
                position = position_dodge(width = 0.3), width = 0.2) +  # Error bars for CI
  scale_color_manual(values = c("blue", "red"), labels = c("Low Pitch Variation", "High Pitch Variation")) +
  labs(title = "Predicted Votes by Decade and Pitch Variation",
       x = "Decade Category",
       y = "Predicted Probability of Voting for Petitioner",
       color = "Pitch Variation") +
  theme_minimal()

# ---------------------------
# Version 2: X-axis = High Pitch Variation, Interaction with Decade Category (Old)
# ---------------------------
fig_c_2 <- ggpredict(m_c_4, terms = c("high_pitch_variation", "decade_category"))

ggplot(fig_c_2, aes(x = x, y = predicted, color = group)) +
  geom_line(size = 1) +  # Line plot for interaction effect
  geom_point(size = 3) +  # Points for means
  geom_ribbon(aes(ymin = conf.low, ymax = conf.high), alpha = 0.2) +  # Confidence interval shading
  scale_color_manual(values = c("blue", "red", "green", "purple"), 
                     labels = unique(fig_c_2$group)) +
  labs(title = "Predicted Votes by Pitch Variation and Decade",
       x = "High Pitch Variation",
       y = "Predicted Probability of Voting for Petitioner",
       color = "Decade") +
  theme_minimal()


# interactions
# are considering decate times the high pitch variation
# Captures if the effect of interest, meaning the effect of the high pitch variation, 
# is different across decades. This realtive to a baseline decade, 
# which is the 1960s. As general rule this will be the first group in our
# categorical variable. 

# So why 1960s and not 1950s? because there is no data for 1950s.

# what to look in tables with interactions:
# 1. Is the slope. Any changes in the slope 
# 2. Are the confidence intervals overlapping? 
#  If they are not overlapping, then we can say that the effect is different across decades.
#  If they do overlap you can not say they are stattistically differnet. 
