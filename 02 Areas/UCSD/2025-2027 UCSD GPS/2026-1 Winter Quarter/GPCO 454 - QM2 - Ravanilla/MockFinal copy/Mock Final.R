# QM 2 Final Exam Part 2
# Name: 
# Date: 


#-------------------#
# SET UP #
#-------------------#

setwd("") # set the working directory
getwd() # check
# load packages
library(tidyverse)
library(ggplot2)
library(interactions)
library(stargazer)
library(modelsummary)
library(ggeffects)
library(margins)
library(lmtest)
library(readxl)
library(car)
library(sandwich)


#-------------------#
# Data Prep #
#-------------------#

# upload data
data = read_excel("part2_final_exam_simulation_data_final.xlsx")
# Question: Does an increase in the share of women in parliament lead to a reduction in
#maternal mortality rates?
# id = women parliament participation
# maternal mortality rates
# To answer this question we need to transform the data columns/variables to become more
#easily interpretable and usable in a regression model. The data has two variables for women’s
#parliament participation: one measurement for 1990 and one measurement for 2010. The
#maternal mortality rate is also provided in the same way: one measurement for 1990 and one
#measurement for 2010. Given this, the best way to make the data more effective to regress, we
#should use the proportional change.

#Step 1: Understanding the data and manipulating it into a more usable format. Remove Inf values and NA's
columns <- colnames(data)[-1]

# remove NAs
data <- data %>%
  mutate(across(all_of(columns), ~ ifelse(.x == ".", NA, .x)),
         across(all_of(columns), as.numeric))

# create parliament change and mortality change variables
data_transformed <- data %>%
  mutate(
    parliament_change = `share-of-women-in-parliament-2010s` - `share-of-women-in-parliament-1990s`,
    parliament_change_percentage =
      ifelse(`share-of-women-in-parliament-1990s` != 0,
             100 * (parliament_change / `share-of-women-in-parliament-1990s`),
             NA),
    mortality_change = `maternal-mortality-2010s` - `maternal-mortality-1990s`,
    mortality_change_percentage = ifelse(`maternal-mortality-1990s` != 0,
                                         100 * (mortality_change / `maternal-mortality-1990s`),
                                         NA)
  ) %>% na.omit ()

#Plotting
ggplot(data = data_transformed,
       aes(x = parliament_change_percentage,
           y = mortality_change_percentage)) +
  geom_point(size = 1, alpha = 0.75) +
  labs(title = "Plotting Women’s Parliament Share Against Maternal Mortality Rate",
       x = "Representation in Parliament as a Percentage",
       y = "Change of Maternal Mortality Rate as a Percentage",
       caption = "Describe the figure here.\nSeparate lines by using \\n or add caption in the write-up"
  ) # save the graph


#-------------------#
# Robustness: trim extreme parliament % change #
#-------------------#

#Outliers
data_clean <- data_transformed %>%
  na.omit() %>%
  filter(abs(parliament_change_percentage) < 1000)

#Plot without Outliers
ggplot(data = data_clean,
       aes(x = parliament_change_percentage,
           y = mortality_change_percentage)) +
  geom_point(size = 1, alpha = 0.75) +
  labs(title = "Plotting Women’s Parliament Share Against Maternal Mortality Rate",
       x = "Representation in Parliament as a Percentage",
       y = "Change of Maternal Mortality Rate as a Percentage",
       caption = "Describe the figure here.\nSeparate lines by using \\n or add caption in thewrite-up"
  )


#-------------------#
# Regression Analysis #
#-------------------#

# start by creating a simple bivariate regression as the base model
#Regressions
# start by creating a simple bivariate regression as the base model
# set the bivariate regression model putting mortality percentage as the dependent variable and
#the parliament change in the independent variable
# models (no vcov argument inside lm)

base_model <- lm(mortality_change_percentage ~ parliament_change_percentage,
                 data = data_clean)

model2 <- lm(mortality_change_percentage ~ parliament_change_percentage +
               `gdp-per-capita-worldbank-2020`,
             data = data_clean)

model3 <- lm(mortality_change_percentage ~ parliament_change_percentage +
               `gdp-per-capita-worldbank-2020` +
               `democracy-index-eiu-2020`,
             data = data_clean)

model4 <- lm(mortality_change_percentage ~ parliament_change_percentage +
               `gdp-per-capita-worldbank-2020` +
               `democracy-index-eiu-2020` +
               `ti-corruption-perception-index-2018`,
             data = data_clean)

# HC1 robust standard errors for each model
robust_se <- list(
  sqrt(diag(vcovHC(base_model, type = "HC1"))),
  sqrt(diag(vcovHC(model2,     type = "HC1"))),
  sqrt(diag(vcovHC(model3,     type = "HC1"))),
  sqrt(diag(vcovHC(model4,     type = "HC1")))
)

stargazer(
  base_model, model2, model3, model4,
  type = "text",
  title = "Regression Results: Mortality Change vs Women in Parliament",
  dep.var.labels = "Mortality change (%)",
  covariate.labels = c(
    "Women in parliament change (%)",
    "GDP per capita (World Bank, 2020)",
    "Democracy Index (EIU, 2020)",
    "Corruption Perceptions Index (TI, 2018)"
  ),
  se = robust_se,
  omit.stat = c("f", "ser"),        # keep what you want
  add.lines = list(
    c("Robust SEs", "HC1", "HC1", "HC1", "HC1")
  ),
  notes = "HC1 robust standard errors in parentheses.",
  out = "Table.txt"
)


#-------------------#
# Checking GM Assumptions #
#-------------------#

#NonLinearity (Use Residual Plot) #We don't log any of the variables (main IV and DV) because
#they are in percent changes with negative numbers (and logging will cause issues that lead to bias)

data_clean$residuals <- model4$residuals
data_clean$fittedvals <- model4$fitted.values
mean(data_clean$residuals)

# what we want: Random scatter around 0, No clear pattern or curve, Roughly constant spread of residuals across fitted values
data_clean %>%
  ggplot(aes(x=fittedvals, y=residuals)) +
  geom_point() +
  geom_hline(yintercept=0, linetype = "dashed", color = "red")

#Multicollinearity (One option is to use VIF)
vif(model4) # =1 (no multicollinearity); 1 to 5 (moderate correlation, usually not problematic); >10 (severe multicollinearity)

#Non-Random Sampling (External and Internal Validity -> qualitative)
#Endogeneity (OVB, Measurement error, Reverse Causaility -> qualitative)
#Use robust std errors

#HC1 is a type of heteroskedasticity-robust variance estimator used to correct the standard errors in a regression.
coeftest(model4, vcov = vcovHC(model4, type = "HC1"))


#BP and White Test
bptest(model4) #Low p-value suggests heteroskedasticity (non constant variance) <0.05
bptest(model4, ~ fitted(model4) + I(fitted(model4)^2)) #Low p-value -> reject null that variance is constant -> suggests heteroskedasticity

#Non-Normal Distribution: Outlier Check
# Calculate outlier diagnostics
stud_resid <- rstudent(model4) # Studentized Residuals
leverage <- hatvalues(model4) # Leverage
cooksd <- cooks.distance(model4) # Cook's Distance
dffits <- dffits(model4) # DFFITS
View(stud_resid)

# Create a dataframe to store outlier diagnostics
outlier_df <- data.frame(
  obs = 1:length(stud_resid),
  abs_stud_resid = abs(stud_resid),
  leverage = leverage,
  abs_dffits = abs(dffits),
  cooksd = cooksd
)


#-------------------#
# Rerun Regression without Outliers #
#-------------------#

# Define Critical Thresholds for Outliers
k <- length(coef(model4)) # Number of predictors
n <- nobs(model4) # Sample size
crit_leverage <- (2 * k + 2) / n #(2*k + 2)/n results in similar results plot wise
crit_cooks <- 4 / n
crit_dffit <- 2 * sqrt(k / n)
# Identify Outliers Based on Thresholds
outlier_df$outlier <- ifelse(
  abs(stud_resid) > 2 | leverage > crit_leverage | cooksd > crit_cooks | abs(dffits) > crit_dffit,
  1, 0
)
data_nooutliers <- data_clean[outlier_df$outlier == 0,]

base_model <- lm(
  mortality_change_percentage ~ parliament_change_percentage,
  data = data_nooutliers
)

model2 <- lm(
  mortality_change_percentage ~ parliament_change_percentage +
    `gdp-per-capita-worldbank-2020`,
  data = data_nooutliers
)

model3 <- lm(
  mortality_change_percentage ~ parliament_change_percentage +
    `gdp-per-capita-worldbank-2020` +
    `democracy-index-eiu-2020`,
  data = data_nooutliers
)

model4 <- lm(
  mortality_change_percentage ~ parliament_change_percentage +
    `gdp-per-capita-worldbank-2020` +
    `democracy-index-eiu-2020` +
    `ti-corruption-perception-index-2018`,
  data = data_nooutliers
)

# HC1 robust standard errors + p-values for stars
robust_se <- list(
  sqrt(diag(vcovHC(base_model, type = "HC1"))),
  sqrt(diag(vcovHC(model2,     type = "HC1"))),
  sqrt(diag(vcovHC(model3,     type = "HC1"))),
  sqrt(diag(vcovHC(model4,     type = "HC1")))
)

robust_p <- list(
  coeftest(base_model, vcov. = vcovHC(base_model, type = "HC1"))[, 4],
  coeftest(model2,     vcov. = vcovHC(model2,     type = "HC1"))[, 4],
  coeftest(model3,     vcov. = vcovHC(model3,     type = "HC1"))[, 4],
  coeftest(model4,     vcov. = vcovHC(model4,     type = "HC1"))[, 4]
)

# Create regression table
stargazer(
  base_model, model2, model3, model4,
  type = "text",
  title = "Regression Results (No Outliers)",
  dep.var.labels = "Mortality change (%)",
  covariate.labels = c(
    "Women in parliament change (%)",
    "GDP per capita (World Bank, 2020)",
    "Democracy Index (EIU, 2020)",
    "Corruption Perceptions Index (TI, 2018)"
  ),
  se = robust_se,
  p  = robust_p,
  omit.stat = c("f", "ser"),        # keep what you want
  add.lines = list(
    c("Robust SEs", "HC1", "HC1", "HC1", "HC1")
  ),
  notes = "HC1 robust standard errors in parentheses."
)