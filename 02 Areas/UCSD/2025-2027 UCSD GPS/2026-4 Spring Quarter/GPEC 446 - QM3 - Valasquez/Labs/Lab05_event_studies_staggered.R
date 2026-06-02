# =============================================================================
#  GPEC 446 — Lab 5: Event Studies and Staggered Difference-in-Differences
# =============================================================================
#
#    1. From DiD to event time — constructing treatment variables
#    2. TWFE and the event study plot
#    3. The Goodman-Bacon decomposition — what is TWFE actually estimating?
#    4. A modern fix — Callaway & Sant'Anna (2021)
#
#  Data: mpdta (from the `did` package)
#        500 US counties × 5 years (2003–2007)
#        County-level teen employment and minimum wage increases
#
#  Context: Between 2004 and 2007, several US counties experienced minimum
#  wage increases above the federal level. Different counties saw increases
#  in different years — a classic case of staggered adoption. We want to
#  estimate how these minimum wage increases affected teen employment.
#
# =============================================================================

library(tidyverse)
library(fixest)
library(bacondecomp)
library(did)


# =============================================================================
# Load and explore the data
# =============================================================================

data(mpdta)
df <- mpdta

# What do we have?
cat("Counties:", n_distinct(df$countyreal), "\n")
cat("Years:   ", min(df$year), "-", max(df$year), "\n")
cat("Obs:     ", nrow(df), "\n\n")

# The outcome: log(teen employment)
# A decrease means fewer teens employed
summary(df$lemp)

# The treatment timing: first.treat
# 0 = never treated; 2004, 2006, 2007 = year of first min wage increase
df %>%
  distinct(countyreal, first.treat) %>%
  count(first.treat)


# =============================================================================
# SECTION 1: From DiD to Event Time
# =============================================================================

# In Lab 4, every treated state had the same "before" and "after".
# Here, minimum wage increases happen at different times for different counties.
# We need to build the event-time structure ourselves.

# ---- Step 1a: Create the binary treatment indicator -------------------------
# treat = 1 in all periods on or after the first min wage increase

df <- df %>%
  mutate(treat = ifelse(first.treat > 0 & year >= first.treat, 1, 0))

# Check: how many county-years are treated?
table(df$treat)

# ---- Step 1b: Create event time (tau) ---------------------------------------
# tau = year - first.treat
# tau = 0 is the year of the minimum wage increase
# tau < 0 is pre-treatment, tau > 0 is post-treatment

df <- df %>%
  mutate(tau = ifelse(first.treat > 0, year - first.treat, NA))

# What does the distribution of event time look like?
table(df$tau)

# ---- Step 1c: Ever-treated indicator ----------------------------------------
df <- df %>%
  mutate(ever_treated = ifelse(first.treat > 0, 1, 0))

cat("\nEver treated:", sum(df$ever_treated & df$year == 2003),
    "counties\n")
cat("Never treated:", sum(!df$ever_treated & df$year == 2003),
    "counties\n")


# =============================================================================
# SECTION 2: TWFE and the Event Study
# =============================================================================

# ---- 2a: Static TWFE — one coefficient for the treatment --------------------
# This is the same approach as Lab 4, Section 3: Y = alpha_i + lambda_t + delta*D + e

mod_twfe <- feols(
  lemp ~ treat | countyreal + year,
  cluster = ~countyreal,
  data   = df
)

summary(mod_twfe)

# QUESTION: Is the coefficient positive or negative? What does it mean
# for teen employment?

# ---- 2b: Event study — one coefficient per event-time period ----------------
# Instead of a single "treat" dummy, we estimate a separate effect for
# each period relative to treatment. We omit tau = -1 as the reference.

# Prepare: make tau a factor with -1 as reference
df_es <- df %>%
  filter(!is.na(tau)) %>%
  mutate(tau_f = relevel(factor(tau), ref = "-1"))

mod_event <- feols(
  lemp ~ i(tau_f, ref = "-1") | countyreal + year,
  cluster = ~countyreal,
  data   = df_es
)

summary(mod_event)


# ---- 2c: Plot the event study -----------------------------------------------

# Extract coefficients and standard errors
coefs <- data.frame(
  tau      = as.numeric(gsub("tau_f::", "", names(coef(mod_event)))),
  estimate = coef(mod_event),
  se       = se(mod_event)
)

# Add the omitted reference period (tau = -1, estimate = 0)
coefs <- bind_rows(
  coefs,
  data.frame(estimate = 0, se = 0, tau = -1)
) %>%
  arrange(tau)

p_twfe_es <- ggplot(coefs, aes(x = tau, y = estimate)) +
  geom_hline(yintercept = 0, colour = "darkred", linetype = "dashed") +
  geom_vline(xintercept = -0.5, colour = "steelblue", linetype = "dashed") +
  geom_point(size = 2) +
  geom_errorbar(aes(ymin = estimate - 1.96 * se,
                     ymax = estimate + 1.96 * se),
                width = 0.2) +
  labs(
    title = "Event Study: Minimum Wage and Teen Employment (TWFE)",
    x     = "Years Before/After Min Wage Increase",
    y     = "Change in log(Employment)"
  ) +
  theme_minimal(base_size = 13)

p_twfe_es
ggsave("fig_twfe_event_study.pdf", p_twfe_es, width = 7, height = 4.5)

# =============================================================================
# SECTION 3: The Goodman-Bacon Decomposition
# =============================================================================

# ---- 3a: Run the decomposition ----------------------------------------------
# With only 500 counties and 5 years, this runs quickly — no subsampling needed.

bacon_out <- bacon(
  lemp ~ treat,
  data     = df,
  id_var   = "countyreal",
  time_var = "year"
)

# What does it return? Each row is one 2x2 comparison.
head(bacon_out)

# The overall TWFE estimate is the weighted average:
cat("\nTWFE estimate (from Bacon):",
    round(weighted.mean(bacon_out$estimate, bacon_out$weight), 4), "\n")
cat("TWFE estimate (from feols):",
    round(coef(mod_twfe)["treat"], 4), "\n")


# ---- 3b: Summarise by comparison type ---------------------------------------

bacon_summary <- bacon_out %>%
  group_by(type) %>%
  summarise(
    n_comparisons = n(),
    total_weight  = round(sum(weight), 3),
    weighted_est  = round(weighted.mean(estimate, weight), 4),
    .groups = "drop"
  )

print(bacon_summary)


# =============================================================================
# SECTION 4: A Modern Fix — Callaway & Sant'Anna (2021)
# =============================================================================

# ---- 4a: Estimate group-time ATTs -------------------------------------------
# gname = the variable identifying each unit's treatment cohort
# Never-treated units already have first.treat = 0, which is what att_gt expects.

mod_cs <- att_gt(
  yname     = "lemp",
  tname     = "year",
  idname    = "countyreal",
  gname     = "first.treat",
  xformla   = ~1,
  data      = df,
  panel     = TRUE,
  clustervars = "countyreal"
)

# This estimates ATT(g,t) for every group-time combination
summary(mod_cs)


# ---- 4b: Aggregate into an event study --------------------------------------

es_cs <- aggte(mod_cs, type = "dynamic")
summary(es_cs)


# ---- 4c: Plot and compare ---------------------------------------------------

# C&S event study
p_cs_es <- ggdid(es_cs) +
  labs(
    title = "Event Study: Callaway & Sant'Anna (2021)",
    x     = "Years Before/After Min Wage Increase",
    y     = "ATT on log(Employment)"
  ) +
  theme_minimal(base_size = 13)

p_cs_es
ggsave("fig_cs_event_study.pdf", p_cs_es, width = 7, height = 4.5)


# ---- 4d: Side-by-side comparison --------------------------------------------
# Let's put both event studies on the same plot

# TWFE estimates (from Section 2)
twfe_es <- coefs %>%
  select(tau, estimate, se) %>%
  mutate(method = "TWFE")

# C&S estimates
cs_es <- data.frame(
  tau      = es_cs$egt,
  estimate = es_cs$att.egt,
  se       = es_cs$se.egt,
  method   = "Callaway & Sant'Anna"
)

# Combine and plot
p_compare <- bind_rows(twfe_es, cs_es) %>%
  filter(tau >= -4, tau <= 3) %>%
  ggplot(aes(x = tau, y = estimate, colour = method)) +
  geom_hline(yintercept = 0, linetype = "dashed", colour = "grey40") +
  geom_vline(xintercept = -0.5, linetype = "dashed", colour = "grey70") +
  geom_point(position = position_dodge(width = 0.4), size = 2) +
  geom_errorbar(
    aes(ymin = estimate - 1.96 * se, ymax = estimate + 1.96 * se),
    width = 0.3,
    position = position_dodge(width = 0.4)
  ) +
  labs(
    title  = "TWFE vs. Callaway & Sant'Anna Event Studies",
    x      = "Years Before/After Min Wage Increase",
    y      = "Change in log(Employment)",
    colour = NULL
  ) +
  theme_minimal(base_size = 13) +
  theme(legend.position = "bottom")

p_compare
ggsave("fig_compare_event_studies.pdf", p_compare, width = 7, height = 4.5)

# =============================================================================
# Lab 5 End
# =============================================================================

