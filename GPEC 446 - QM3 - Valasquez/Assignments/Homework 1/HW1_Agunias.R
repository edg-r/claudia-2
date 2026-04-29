# =============================================================================
#  GPEC 446 — Homework 1
#  Neighborhoods, Upward Mobility, and Instrumental Variables
#  Edgar Agunias
#  Last modified: 04.20.2026
# =============================================================================
#
#  Builds directly on Lab 1 (randomisation / balance / regression-as-
#  difference-in-means) and Lab 2 (regression as stratification, omitted
#  variable bias, simultaneity).  Lab 2 is the closest analog for Questions 3-6:
#  we run a "short" regression, a "long" regression, and decompose the
#  difference using the OVB formula  (OVB = pi_1 * gamma).
#
#  Data:
#    - atlas.csv         — Opportunity Atlas tract-level extract
#    - AER::Fertility2   — Angrist & Evans (1998) replication sample
#
# =============================================================================


# -----------------------------------------------------------------------------
# SETUP
# -----------------------------------------------------------------------------

library(AER)          # Fertility2 data and ivreg()
library(tidyverse)    # dplyr + ggplot2 + readr
library(stargazer)    # publication-style regression tables (as in both labs)


# -----------------------------------------------------------------------------
# SECTION 1 — Load and Prepare the Opportunity Atlas Data
# -----------------------------------------------------------------------------
#
#  This section mirrors Lab 1 §2 and Lab 2 §1b/§2a: load, inspect, and build
#  the indicator / rescaled variables we will use throughout.

atlas_raw <- read_csv("atlas.csv", show_col_types = FALSE)

cat("Number of tracts:", nrow(atlas_raw), "\n")
cat("Number of commuting zones:", length(unique(atlas_raw$czname)), "\n\n")

# Build the working dataset.
#   - majority_non_white: indicator (1 if white share < 0.5 in 2000)
#   - poverty_pp: 1990 poverty share on a percentage-point scale
#   - mobility_k: child income at p25 parents, in $1000s
#   - fips: 11-digit census tract FIPS (2 state + 3 county + 6 tract)
#
# FIPS construction note:
#   The atlas stores `tract` as the 6-digit census tract code. Values range
#   from 3 to 6 digits depending on state/county numbering, so we zero-pad.
#   All three components are integers (verified: tracts <= 999999,
#   counties <= 999, states <= 99).

atlas <- atlas_raw %>%
  mutate(
    majority_non_white = as.numeric(share_white2000 < 0.5),
    poverty_pp         = poor_share1990 * 100,
    mobility_k         = kfr_pooled_p25 / 1000,
    fips               = sprintf("%02d%03d%06d",
                                 as.integer(state),
                                 as.integer(county),
                                 as.integer(tract))
  )

# Quick sanity check: every FIPS should be exactly 11 characters.
stopifnot(all(nchar(atlas$fips) == 11L))

# Summary statistics for the headline variables (Lab 2 §2a pattern).
atlas %>%
  select(mobility_k, poverty_pp, majority_non_white, popdensity2000) %>%
  as.data.frame() %>%
  stargazer(type = "text",
            title = "Summary Statistics — Opportunity Atlas Tracts",
            covariate.labels = c("Child Income at p25 ($1000s)",
                                 "Poverty Rate 1990 (pp)",
                                 "Majority Non-White (= 1)",
                                 "Population Density 2000"),
            digits = 2)


# -----------------------------------------------------------------------------
# SECTION 2 — Questions 1 & 2: Descriptive Look at One City / One Tract
# -----------------------------------------------------------------------------
#
#  Lab 1 §2 style: use dplyr verbs to filter, arrange, and summarise.

chosen_city <- "New Orleans"
chosen_city_data <- atlas %>% filter(czname == chosen_city)

cat("Tracts in", chosen_city, ":", nrow(chosen_city_data), "\n")

# The highest-mobility tract in the chosen city
chosen_tract <- chosen_city_data %>%
  filter(!is.na(kfr_pooled_p25)) %>%
  arrange(desc(kfr_pooled_p25)) %>%
  slice(1)

cat("Highest-mobility tract FIPS:", chosen_tract$fips, "\n")
cat("Tract mobility ($):         ", round(chosen_tract$kfr_pooled_p25, 0), "\n")

# City and state benchmarks
chosen_city_mean <- mean(chosen_city_data$kfr_pooled_p25, na.rm = TRUE)
chosen_city_sd   <- sd(chosen_city_data$kfr_pooled_p25,   na.rm = TRUE)
chosen_state_sd  <- atlas %>%
  filter(state == chosen_tract$state) %>%
  summarise(sd_state = sd(kfr_pooled_p25, na.rm = TRUE)) %>%
  pull(sd_state)

cat("City mean mobility ($):  ", round(chosen_city_mean, 0), "\n")
cat("City SD mobility ($):    ", round(chosen_city_sd,   0), "\n")
cat("State SD mobility ($):   ", round(chosen_state_sd,  0), "\n")


# -----------------------------------------------------------------------------
# SECTION 3 — Question 3: Poverty and Mobility in Four Cities
# -----------------------------------------------------------------------------
#
#  This is the Lab 2 §2h visualisation pattern (ggplot + geom_smooth) applied
#  across four commuting zones. For each city we also fit a simple
#  mobility_k ~ poverty_pp regression.

cities <- c("Los Angeles", "New York", "Chicago", "New Orleans")
city_data <- atlas %>% filter(czname %in% cities)

# Scatter + fitted line per city
ggplot(city_data, aes(x = poverty_pp, y = kfr_pooled_p25)) +
  geom_point(alpha = 0.25, size = 1, colour = "#1f4e79") +
  geom_smooth(method = "lm", se = FALSE, colour = "#b22222", linewidth = 1) +
  facet_wrap(~ czname, scales = "free") +
  labs(
    title    = "Tract poverty and upward mobility, four cities",
    subtitle = "Higher tract poverty is associated with lower mobility in all four cities",
    x        = "Poverty rate in 1990 (percentage points)",
    y        = "Child income for p25 parents ($)"
  ) +
  theme_minimal(base_size = 12)

# One simple regression per city — same pattern as Lab 2 reg_short.
reg_la  <- lm(mobility_k ~ poverty_pp, data = filter(atlas, czname == "Los Angeles"))
reg_ny  <- lm(mobility_k ~ poverty_pp, data = filter(atlas, czname == "New York"))
reg_chi <- lm(mobility_k ~ poverty_pp, data = filter(atlas, czname == "Chicago"))
reg_no  <- lm(mobility_k ~ poverty_pp, data = filter(atlas, czname == "New Orleans"))

stargazer(reg_la, reg_ny, reg_chi, reg_no,
          type = "text",
          title = "Poverty and Mobility: Simple Regressions by City",
          column.labels = c("Los Angeles", "New York", "Chicago", "New Orleans"),
          dep.var.labels = "Child Income at p25 ($1000s)",
          covariate.labels = c("Poverty Rate 1990 (pp)"),
          omit.stat = c("f", "ser"),
          notes = c("One simple OLS per city. Coefficient = $1000 change in",
                    "mobility per 1pp increase in tract poverty."))


# -----------------------------------------------------------------------------
# SECTION 4 — Questions 4 & 5: OVB and Interaction (New Orleans)
# -----------------------------------------------------------------------------
#
#  Direct analog to Lab 2 §2b–§2f.
#
#    reg_short  = mobility_k ~ poverty_pp                     (Model 3)
#    reg_long   = mobility_k ~ poverty_pp + majority_non_white (Model 4)
#    reg_intx   = mobility_k ~ poverty_pp * majority_non_white (Model 5)
#
#  OVB formula:   OVB = pi_1 * gamma
#    pi_1  = coefficient from auxiliary regression of the omitted variable
#            (majority_non_white) on the explanatory variable (poverty_pp)
#    gamma = coefficient on majority_non_white in the long regression

no_data <- atlas %>% filter(czname == "New Orleans")

reg_short <- lm(mobility_k ~ poverty_pp,                      data = no_data)
reg_long  <- lm(mobility_k ~ poverty_pp + majority_non_white, data = no_data)
reg_intx  <- lm(mobility_k ~ poverty_pp * majority_non_white, data = no_data)

# Auxiliary regression for the OVB decomposition — same pattern as Lab 2 §2e.
aux_reg <- lm(majority_non_white ~ poverty_pp, data = no_data)

beta_short <- coef(reg_short)[["poverty_pp"]]
beta_long  <- coef(reg_long)[["poverty_pp"]]
pi_1       <- coef(aux_reg)[["poverty_pp"]]
gamma_hat  <- coef(reg_long)[["majority_non_white"]]

ovb_actual  <- beta_short - beta_long
ovb_formula <- pi_1 * gamma_hat

cat("\n--- OVB Formula Verification (New Orleans) ---\n")
cat("beta_short (poverty_pp, no controls):", round(beta_short, 4), "\n")
cat("beta_long  (poverty_pp, + race):     ", round(beta_long,  4), "\n")
cat("pi_1   (mnw ~ poverty_pp):           ", round(pi_1,       4), "\n")
cat("gamma  (mnw in long reg):            ", round(gamma_hat,  4), "\n")
cat("OVB (actual: short - long):          ", round(ovb_actual, 4), "\n")
cat("OVB (formula: pi_1 * gamma):         ", round(ovb_formula, 4), "\n")
cat("Match?", abs(ovb_formula - ovb_actual) < 1e-3, "\n")

#  Sign table (Lab 2 §2f logic):
#    pi_1 > 0   (higher poverty tracts are more likely majority non-white)
#    gamma < 0  (majority non-white tracts have lower mobility)
#    => OVB < 0  (the short regression makes the poverty slope look too negative)

# Models 3, 4, 5 side by side — stargazer instead of kable (Lab 2 convention).
stargazer(reg_short, reg_long, reg_intx,
          type = "text",
          title = "New Orleans: Poverty, Race, and Upward Mobility",
          column.labels = c("Short (Q3)", "Long (Q4)", "Interaction (Q5)"),
          dep.var.labels = "Child Income at p25 ($1000s)",
          covariate.labels = c("Poverty Rate 1990 (pp)",
                               "Majority Non-White (= 1)",
                               "Poverty x Majority Non-White"),
          omit.stat = c("f", "ser"),
          notes = c("Sample: New Orleans commuting zone tracts.",
                    "Coefficient units: $1000s per pp of poverty."))


# -----------------------------------------------------------------------------
# SECTION 5 — Question 6: Causal Interpretation (discussion)
# -----------------------------------------------------------------------------
#
#  No new estimation. The answer lives in the .Rmd; conceptually this is the
#  Lab 2 §3 lesson: controls cannot cure every endogeneity problem. Poverty
#  and racial composition are not randomly assigned, and many confounders
#  (school quality, policing, segregation, local labor markets) remain.


# -----------------------------------------------------------------------------
# SECTION 6 — Questions 7-9: National Regression + Commuting-Zone FE
# -----------------------------------------------------------------------------
#
#  Replicate Model 4 on the pooled national sample, then add commuting-zone
#  fixed effects. This is the Dale-Krueger "within choice set" analogy.

reg_all      <- lm(mobility_k ~ poverty_pp + majority_non_white,                data = atlas)
reg_all_fe   <- lm(mobility_k ~ poverty_pp + majority_non_white + factor(cz),   data = atlas)

stargazer(reg_all, reg_all_fe,
          type = "text",
          title = "National Sample: Pooled OLS vs. Commuting-Zone FE",
          column.labels = c("Pooled OLS", "+ CZ Fixed Effects"),
          dep.var.labels = "Child Income at p25 ($1000s)",
          covariate.labels = c("Poverty Rate 1990 (pp)",
                               "Majority Non-White (= 1)"),
          omit = "factor\\(cz\\)",
          omit.stat = c("f", "ser"),
          add.lines = list(c("Commuting-zone FE", "No", "Yes")),
          notes = c("CZ fixed effects absorb all between-city variation.",
                    "Identification in column (2) is within-CZ only."))


# -----------------------------------------------------------------------------
# SECTION 7 — Open Question: Urban vs. Rural Mobility
# -----------------------------------------------------------------------------
#
#  Proxy urbanicity with tract population density (2000). Bottom-quartile
#  density = rural proxy; top quartile = urban proxy.

density_breaks <- quantile(atlas$popdensity2000, probs = seq(0, 1, 0.1),
                           na.rm = TRUE)

atlas_open <- atlas %>%
  mutate(
    density_decile = cut(popdensity2000, breaks = density_breaks,
                         include.lowest = TRUE, labels = 1:10),
    density_group = case_when(
      popdensity2000 <= quantile(popdensity2000, 0.25, na.rm = TRUE) ~ "Rural proxy",
      popdensity2000 >= quantile(popdensity2000, 0.75, na.rm = TRUE) ~ "Urban proxy",
      TRUE ~ "Middle 50%"
    )
  )

open_table <- atlas_open %>%
  filter(density_group != "Middle 50%") %>%
  group_by(density_group) %>%
  summarise(
    tracts             = n(),
    mean_mobility      = mean(kfr_pooled_p25,   na.rm = TRUE),
    sd_mobility        = sd(kfr_pooled_p25,     na.rm = TRUE),
    mean_poverty_pp    = mean(poverty_pp,       na.rm = TRUE),
    mean_white_share   = mean(share_white2000 * 100, na.rm = TRUE),
    .groups = "drop"
  )

print(open_table)

open_deciles <- atlas_open %>%
  filter(!is.na(density_decile)) %>%
  group_by(density_decile) %>%
  summarise(
    mean_density  = mean(popdensity2000, na.rm = TRUE),
    mean_mobility = mean(kfr_pooled_p25, na.rm = TRUE),
    mean_poverty  = mean(poverty_pp,     na.rm = TRUE),
    .groups = "drop"
  )

ggplot(open_deciles,
       aes(x = as.numeric(as.character(density_decile)), y = mean_mobility)) +
  geom_line(colour = "#1f4e79", linewidth = 1) +
  geom_point(colour = "#b22222", size = 2) +
  scale_x_continuous(breaks = 1:10) +
  labs(
    title    = "Mean mobility by tract-density decile",
    subtitle = "Denser tracts do not deliver uniformly higher mobility",
    x        = "Population-density decile (1 = sparsest, 10 = densest)",
    y        = "Mean child income at p25 ($)"
  ) +
  theme_minimal(base_size = 12)


# -----------------------------------------------------------------------------
# SECTION 8 — Questions 10 & 11: Instrumental Variable (Angrist-Evans)
# -----------------------------------------------------------------------------
#
#  We want the causal effect of having a third child (morekids) on maternal
#  labor supply (work). The OLS regression of work on morekids is biased by
#  selection — women who want to work may also choose to have fewer kids.
#
#  Instrument: same_gender (= 1 if the first two children share sex). This is
#  plausibly random AND shifts the probability of a third child because some
#  parents want a mixed-sex composition.
#
#  Mechanics below follow the Lab 2 §3 "what would we need to fix this?"
#  setup, but we now have the tool: an IV. We do the three-step version for
#  teaching clarity AND the single call with AER::ivreg() so the standard
#  errors are correct (manual 2SLS SEs are wrong because the second stage
#  treats fitted morekids as if it were observed).

data("Fertility2")

fertility2 <- Fertility2 %>%
  mutate(
    morekids_num = as.numeric(morekids == "yes"),
    same_gender  = as.numeric(gender1 == gender2)
  )

# --- 8a. First stage: does the instrument move the treatment? ---
iv_first_stage  <- lm(morekids_num ~ same_gender, data = fertility2)

# --- 8b. Reduced form: does the instrument move the outcome? ---
iv_reduced_form <- lm(work ~ same_gender, data = fertility2)

# --- 8c. Manual 2SLS (wrong SEs, right point estimate) ---
fertility2 <- fertility2 %>%
  mutate(morekids_hat = fitted(iv_first_stage))
iv_second_stage <- lm(work ~ morekids_hat, data = fertility2)

# --- 8d. Correct 2SLS via AER::ivreg() (right SEs) ---
#   Syntax: ivreg(outcome ~ endog | instrument, data = ...)
iv_aer <- ivreg(work ~ morekids_num | same_gender, data = fertility2)

stargazer(iv_first_stage, iv_reduced_form, iv_second_stage, iv_aer,
          type = "text",
          title = "Angrist-Evans IV: Same-Sex Instrument for Third Child",
          column.labels = c("1st Stage", "Reduced Form",
                            "Manual 2SLS", "AER ivreg()"),
          dep.var.labels.include = TRUE,
          covariate.labels = c("Same Gender (instrument)",
                               "Predicted More Kids (manual 2SLS)",
                               "More Kids (IV)"),
          omit.stat = c("f", "ser"),
          notes = c("Manual 2SLS point estimate equals ivreg() point estimate,",
                    "but manual 2SLS standard errors are understated.",
                    "Use ivreg() for inference."))

cat("\nFirst-stage coefficient (same_gender):",
    round(coef(iv_first_stage)[["same_gender"]], 4), "\n")
cat("Reduced-form coefficient (same_gender):",
    round(coef(iv_reduced_form)[["same_gender"]], 4), "\n")
cat("Manual 2SLS:", round(coef(iv_second_stage)[["morekids_hat"]], 4),
    " SE:", round(summary(iv_second_stage)$coef["morekids_hat", "Std. Error"], 4), "\n")
cat("AER ivreg:  ", round(coef(iv_aer)[["morekids_num"]], 4),
    " SE:", round(summary(iv_aer)$coef["morekids_num", "Std. Error"], 4), "\n")
cat("Wald check (RF / FS):",
    round(coef(iv_reduced_form)[["same_gender"]] /
          coef(iv_first_stage)[["same_gender"]], 4), "\n")


# =============================================================================
# End of HW1
# =============================================================================
