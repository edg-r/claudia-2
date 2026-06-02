# ======================================================================
#  GPEC 446 — Lab 6: Regression Discontinuity Design
#  Application: Incumbency Advantage in US Senate Elections (Lee, 2008)
# ======================================================================

# --- Packages ---------------------------------------------------------
library(tidyverse)
library(rdrobust)
library(rddensity)
library(stargazer)
library(modelsummary)

# --- Helper: teach modelsummary how to read rdrobust objects -----------
# Define tidy() and glance() methods so modelsummary can extract
# coefficients and goodness-of-fit stats from rdrobust objects.

tidy.rdrobust <- function(x, ...) {
  data.frame(
    term      = "RD Estimate",
    estimate  = x$Estimate[, "tau.bc"],
    std.error = x$Estimate[, "se.rb"],
    p.value   = x$pv[3],
    conf.low  = x$ci[3, 1],
    conf.high = x$ci[3, 2]
  )
}

glance.rdrobust <- function(x, ...) {
  data.frame(
    `Bandwidth (left)`  = round(x$bws[1, 1], 3),
    `Bandwidth (right)` = round(x$bws[1, 2], 3),
    `N (left)`          = x$N_h[1],
    `N (right)`         = x$N_h[2],
    `Polynomial`        = x$p,
    check.names = FALSE
  )
}

# --- 1. Load and prepare data -----------------------------------------

data(rdrobust_RDsenate)
df <- rdrobust_RDsenate
names(df) <- c("margin", "vote_next")

# margin    = Democratic vote share margin in election t (running variable)
# vote_next = Democratic vote share in election t+1 (outcome)
# cutoff: margin = 0  (Democrat wins if margin >= 0)

# --- 2. Visualising the discontinuity ---------------------------------

# 2a. Raw scatterplot with cutoff
ggplot(df, aes(x = margin, y = vote_next)) +
  geom_point(alpha = 0.3, size = 1) +
  geom_vline(xintercept = 0, linetype = "dashed", colour = "red") +
  labs(
    x = "Democratic margin of victory, election t",
    y = "Democratic vote share, election t+1",
    title = "RDD: Incumbency Advantage in US Senate"
  ) +
  theme_minimal()

# 2b. Binned scatterplot with bin means
# Create bins of the running variable and compute mean outcome in each bin
bin_width <- 5  # width of bins in percentage points
df_bins <- df %>%
  mutate(bin = floor(margin / bin_width) * bin_width + bin_width / 2) %>%
  group_by(bin) %>%
  summarise(
    vote_mean = mean(vote_next, na.rm = TRUE),
    n = n(),
    .groups = "drop"
  )

ggplot(df_bins, aes(x = bin, y = vote_mean)) +
  geom_point(size = 2) +
  geom_vline(xintercept = 0, linetype = "dashed", colour = "red") +
  labs(
    x = "Democratic margin of victory, election t (bin midpoint)",
    y = "Mean Democratic vote share, election t+1",
    title = "RDD: Binned Scatterplot"
  ) +
  theme_minimal()

# 2c. With separate linear fits on each side
ggplot(df, aes(x = margin, y = vote_next)) +
  geom_point(alpha = 0.2, size = 1) +
  geom_vline(xintercept = 0, linetype = "dashed", colour = "red") +
  geom_smooth(
    data = filter(df, margin < 0),
    method = "lm", formula = y ~ x, se = TRUE, colour = "steelblue"
  ) +
  geom_smooth(
    data = filter(df, margin >= 0),
    method = "lm", formula = y ~ x, se = TRUE, colour = "steelblue"
  ) +
  labs(
    x = "Democratic margin of victory, election t",
    y = "Democratic vote share, election t+1",
    title = "RDD: Linear Fits on Each Side of Cutoff"
  ) +
  theme_minimal()

# 2d. Binned scatterplot + linear fits combined
ggplot() +
  geom_point(data = df_bins, aes(x = bin, y = vote_mean), size = 2) +
  geom_smooth(
    data = filter(df, margin < 0), aes(x = margin, y = vote_next),
    method = "lm", formula = y ~ x, se = T, colour = "steelblue"
  ) +
  geom_smooth(
    data = filter(df, margin >= 0), aes(x = margin, y = vote_next),
    method = "lm", formula = y ~ x, se = T, colour = "steelblue"
  ) +
  geom_vline(xintercept = 0, linetype = "dashed", colour = "red") +
  labs(
    x = "Democratic margin of victory, election t",
    y = "Democratic vote share, election t+1",
    title = "RDD: Bins + Linear Fit"
  ) +
  theme_minimal()


# --- 3. Manual estimation (building intuition) ------------------------

# 3a. Choose a bandwidth and trim the sample
h <- 10
df_window <- df %>%
  filter(abs(margin) <= h) %>%
  mutate(D = ifelse(margin >= 0, 1, 0))

nrow(df_window)

# 3b. Linear, same slope
mod1 <- lm(vote_next ~ D + margin, data = df_window)

# 3c. Linear, different slopes
mod2 <- lm(vote_next ~ D + margin + D * margin, data = df_window)
mod2 <- lm(vote_next ~ D * margin, data = df_window)  # equivalent formula

# Compare the two specifications side by side
stargazer(mod1, mod2,
          type = "text",
          title = "Manual RDD Estimation (h = 10)",
          column.labels = c("Same Slope", "Different Slopes"),
          dep.var.labels = "Dem Vote Share (t+1)",
          covariate.labels = c("D (Treatment)", "Margin",
                               "D x Margin"),
          keep.stat = c("n", "rsq", "adj.rsq"),
          notes = "Bandwidth h = 10 percentage points.")

# 3d. Try different bandwidths
# Estimate the different-slopes model at four bandwidths
bw_models <- list()
for (bw in c(5, 10, 15, 20)) {
  tmp <- df %>%
    filter(abs(margin) <= bw) %>%
    mutate(D = ifelse(margin >= 0, 1, 0))
  bw_models[[paste0("h=", bw)]] <- lm(vote_next ~ D * margin,
                                        data = tmp)
}

stargazer(bw_models,
          type = "text",
          title = "RDD Estimates Across Bandwidths",
          column.labels = names(bw_models),
          dep.var.labels = "Dem Vote Share (t+1)",
          covariate.labels = c("D (Treatment)", "Margin",
                               "D x Margin"),
          keep.stat = c("n", "rsq"))


# --- 4. rdrobust: optimal bandwidth and robust inference --------------

# 4a. Default: local linear, triangular kernel, optimal bandwidth
rd_out <- rdrobust(
  y = df$vote_next,
  x = df$margin,
  c = 0,
  p = 1,          # local linear
)
summary(rd_out)

# 4b. rdplot: binned scatterplot with polynomial fit
rdplot(
  y = df$vote_next,
  x = df$margin,
  c = 0,
  p = 1,
  title = "RDD: Incumbency Advantage in US Senate Elections",
  x.label = "Democratic margin, election t",
  y.label = "Democratic vote share, election t+1"
)

# 4c. Local quadratic
rd_quad <- rdrobust(df$vote_next, df$margin, c = 0, p = 2)
summary(rd_quad)

rdplot(
  y = df$vote_next,
  x = df$margin,
  c = 0,
  p = 2,
  title = "RDD: Incumbency Advantage in US Senate Elections",
  x.label = "Democratic margin, election t",
  y.label = "Democratic vote share, election t+1"
)

# 4d. Kernels: how observations are weighted
#
# Within the bandwidth window, not all observations contribute equally.
# A *kernel* assigns weights based on distance from the cutoff:
#   - Uniform (rectangular): all observations in the window get equal weight
#   - Triangular: weight = 1 - |X_i - x0| / h  (linearly declining)
#   - Epanechnikov: weight = 1 - ((X_i - x0) / h)^2  (quadratic decline)
#
# The triangular kernel is the default in rdrobust and is optimal for
# boundary estimation (i.e., estimating the conditional mean right at
# the cutoff). Observations closer to x0 are more informative about
# the jump, so they should count more.

# Visualise the three kernels
h_vis <- rd_out$bws[1, 1]   # use the optimal bandwidth

df_kernel <- df %>%
  filter(abs(margin) <= h_vis) %>%
  mutate(
    dist = abs(margin) / h_vis,               # normalised distance
    w_uniform      = 1,                        # rectangular
    w_triangular   = 1 - dist,                 # triangular
    w_epanechnikov = 1 - dist^2               # Epanechnikov
  )

# Plot kernel weights vs. distance from cutoff
df_kernel_long <- df_kernel %>%
  select(margin, w_uniform, w_triangular, w_epanechnikov) %>%
  pivot_longer(
    cols = starts_with("w_"),
    names_to = "kernel",
    values_to = "weight",
    names_prefix = "w_"
  ) %>%
  mutate(kernel = str_to_title(kernel))

ggplot(df_kernel_long, aes(x = margin, y = weight, colour = kernel)) +
  geom_line(linewidth = 1) +
  geom_vline(xintercept = 0, linetype = "dashed", colour = "red") +
  labs(
    x = "Democratic margin of victory",
    y = "Kernel weight",
    colour = "Kernel",
    title = paste0("Kernel Weights within Bandwidth (h = ",
                   round(h_vis, 1), ")")
  ) +
  theme_minimal()


# Compare estimates across kernels using rdrobust
rd_tri  <- rdrobust(df$vote_next, df$margin, c = 0,
                    kernel = "triangular")
rd_uni  <- rdrobust(df$vote_next, df$margin, c = 0,
                    kernel = "uniform")
rd_epa  <- rdrobust(df$vote_next, df$margin, c = 0,
                    kernel = "epanechnikov")

# Comparison table using modelsummary (works thanks to tidy/glance above)
modelsummary(
  list("Triangular" = rd_tri, "Uniform" = rd_uni,
       "Epanechnikov" = rd_epa),
  stars     = TRUE,
  gof_map   = c("Bandwidth (left)", "Bandwidth (right)",
                "N (left)", "N (right)"),
  title     = "RDD Estimates by Kernel",
  notes     = "Bias-corrected estimates with robust SEs (Calonico, Cattaneo & Titiunik 2014)."
)


# 4e. Manual bandwidth = 15
rd_h15 <- rdrobust(df$vote_next, df$margin, c = 0, h = 15)
summary(rd_h15)

# Compare polynomial orders and bandwidth choices
modelsummary(
  list("Linear (opt h)" = rd_out, "Quadratic (opt h)" = rd_quad,
       "Linear (h=15)" = rd_h15),
  stars     = TRUE,
  gof_map   = c("Bandwidth (left)", "Bandwidth (right)",
                "N (left)", "N (right)", "Polynomial"),
  title     = "RDD Estimates: Polynomial Order and Bandwidth",
  notes     = "Bias-corrected estimates with robust SEs (Calonico, Cattaneo & Titiunik 2014)."
)


# --- 5. Robustness checks --------------------------------------------

# 5a. Bandwidth sensitivity
h_opt <- rd_out$bws[1, 1]

bandwidths <- seq(0.5 * h_opt, 2 * h_opt, length.out = 10)
results <- data.frame(
  h = bandwidths,
  estimate  = NA,
  ci_lower  = NA,
  ci_upper  = NA
)

for (i in seq_along(bandwidths)) {
  rd_i <- rdrobust(df$vote_next, df$margin, c = 0,
                   h = bandwidths[i])
  results$estimate[i] <- rd_i$coef[1]
  results$ci_lower[i] <- rd_i$ci[3, 1]   # robust CI
  results$ci_upper[i] <- rd_i$ci[3, 2]
}

ggplot(results, aes(x = h, y = estimate)) +
  geom_point() +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.3) +
  geom_hline(yintercept = 0, linetype = "dashed", colour = "grey50") +
  geom_vline(xintercept = h_opt, linetype = "dotted", colour = "red") +
  labs(
    x = "Bandwidth (h)",
    y = "RDD Estimate",
    title = "Bandwidth Sensitivity"
  ) +
  theme_minimal()


# 5b. Placebo cutoffs
placebo_cuts <- c(-20, -10, 10, 20)
placebo_results <- data.frame(
  cutoff   = placebo_cuts,
  estimate = NA,
  pvalue   = NA
)

for (i in seq_along(placebo_cuts)) {
  rd_p <- rdrobust(df$vote_next, df$margin, c = placebo_cuts[i])
  placebo_results$estimate[i] <- rd_p$coef[1]
  placebo_results$pvalue[i]   <- rd_p$pv[3]   # robust p-value
}

placebo_results


# 5c. McCrary density test
dens_test <- rddensity(X = df$margin, c = 0)
summary(dens_test)

rdplotdensity(dens_test, df$margin,
  title  = "McCrary Density Test",
  xlabel = "Democratic margin, election t",
  ylabel = "Density"
)

