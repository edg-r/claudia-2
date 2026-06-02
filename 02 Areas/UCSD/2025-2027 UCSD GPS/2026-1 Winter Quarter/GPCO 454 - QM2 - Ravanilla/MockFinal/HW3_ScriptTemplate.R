# Script for GPCO 454 - Quantitative Methods II - Winter 2025
# End-to-end Homework 3 script.

# ---------------------------
# 1) Setup
# ---------------------------

#setwd('/Users/edgar/Documents/01 Projects/GPCO 454 - QM2 - Ravanilla/HomeWork/HW3')

library(dplyr)     # Data manipulation verbs and piping pipelines
library(tidyr)     # Missing-data helpers and reshaping utilities
library(ggplot2)   # Plot creation and figure export support
library(stargazer) # Regression table formatting for assignment outputs

# Writing plain-text outputs to minimal HTML for clean copy/paste into Word.
html_escape <- function(x) {
  x <- gsub("&", "&amp;", x, fixed = TRUE)
  x <- gsub("<", "&lt;", x, fixed = TRUE)
  x <- gsub(">", "&gt;", x, fixed = TRUE)
  x
}

write_html_pre <- function(lines, file, title = "HW3 Output") {
  html <- c(
    "<!DOCTYPE html>",
    "<html>",
    "<head>",
    "  <meta charset=\"utf-8\">",
    paste0("  <title>", title, "</title>"),
    "  <style>body{font-family:Calibri,Arial,sans-serif;margin:24px;} pre{white-space:pre-wrap;line-height:1.35;}</style>",
    "</head>",
    "<body>",
    "  <pre>",
    html_escape(paste(lines, collapse = "\n")),
    "  </pre>",
    "</body>",
    "</html>"
  )
  writeLines(html, file)
}

# Using this helper to turn each term year into a court-period label.
build_court_period <- function(term_vec) {
  case_when(
    term_vec >= 1969 & term_vec <= 1985 ~ "Burger",
    term_vec >= 1986 & term_vec <= 2004 ~ "Rehnquist",
    term_vec >= 2005 ~ "Roberts",
    TRUE ~ NA_character_
  )
}

# Using this helper to pick the most common category to hold one factor constant in interaction plots.
first_mode <- function(x) {
  tab <- sort(table(x), decreasing = TRUE)
  names(tab)[1]
}

# Using this helper to wrap long plot text so titles and captions do not run off the figure.
wrap_plot_text <- function(x, width = 90) {
  paste(strwrap(x, width = width), collapse = "\n")
}

# Building evenly spaced axis breaks that also label intermediate grid lines.
seq_axis_breaks <- function(x, by, pad = 0) {
  rng <- range(x, na.rm = TRUE)
  seq(floor((rng[1] - pad) / by) * by, ceiling((rng[2] + pad) / by) * by, by = by)
}

# Using this shared theme to keep all figures styled the same way with clean titles and readable notes.
hw3_plot_theme <- theme_minimal() +
  theme(
    plot.title.position = "plot",
    plot.caption.position = "plot",
    plot.title = element_text(size = 12, face = "bold", margin = margin(b = 4)),
    plot.subtitle = element_text(size = 10, margin = margin(b = 8), lineheight = 1.05),
    plot.caption = element_text(face = "italic", hjust = 0, size = 8.5, lineheight = 1.05, margin = margin(t = 8)),
    plot.margin = margin(t = 10, r = 14, b = 14, l = 10)
  )

# Reusing this note for court-period labels shown in multiple figures.
court_period_year_note <- "Court periods: Burger (1969-1985), Rehnquist (1986-2004), Roberts (2005+)."

# ---------------------------
# 2) Section 3.1 Preliminaries
# ---------------------------

# Loading input data into justice_data.
justice_data <- read.table(
  "justice_results.tab",
  header = TRUE,
  sep = "\t",
  encoding = "ISO-8859-1"
)

# Printing structure and overall summaries for quick diagnostics/Q1-Q2 support.
str(justice_data)
summary(justice_data)
View(justice_data) #Opens data for viewing in new tab

# ---------------------------
# 3) Section 3.2 Descriptive Stats and Plots
# ---------------------------

# Calculating required descriptive statistics for key variables (Q5 setup).
summary_3_2 <- summary(justice_data[, c("petitioner_vote", "pitch_diff", "petitioner_harvard_pos")])
print(summary_3_2)

# Building analysis features used in descriptive plots.
pitch_mean <- mean(justice_data$pitch_diff, na.rm = TRUE)
justice_data <- justice_data %>%
  mutate(
    high_pitch_diff = ifelse(pitch_diff > pitch_mean, 1, 0), #if pitch is above the mean then give a 1
    high_pitch_diff = factor(high_pitch_diff, levels = c(0, 1)),                      # Ordered binary factor
    court_period = build_court_period(term),                                           # Term-to-court-period mapping
    court_period = factor(court_period, levels = c("Burger", "Rehnquist", "Roberts")) # Stable plotting/model order
  )

# Doing a quick frequency check on the new helper variables.
table(justice_data$high_pitch_diff, useNA = "ifany")
table(justice_data$court_period, useNA = "ifany")

# For Figure 1, keeping only the three chief justices and the columns actually needed.
chief_data <- justice_data %>%
  filter(justiceName %in% c("WEBurger", "WHRehnquist", "JGRoberts")) %>%
  select(justiceName, petitioner_vote, sgpetac) %>%
  drop_na()

# Calculating petitioner-vote share by justice and Solicitor General amicus status 1= filed 0 = not filed.
fig1_summary <- chief_data %>%
  group_by(justiceName, sgpetac) %>% 
  summarise(prop_petitioner_vote = mean(petitioner_vote), .groups = "drop") %>%
  mutate(
    sgpetac_label = ifelse(sgpetac == 1, "Amicus", "No Amicus"), #creates a dummy where if the SG filed it is labeld amicus
    sgpetac_label = factor(sgpetac_label, levels = c("No Amicus", "Amicus"))
  )

# Building Figure 1 bar chart with assignment colors and y-range.
# Creating the ggplot object and storing it in p1.
p1 <- ggplot(fig1_summary, aes(x = sgpetac_label, y = prop_petitioner_vote, fill = sgpetac_label)) +
  geom_col() +
  facet_wrap(~ justiceName) +
  scale_fill_manual(values = c("No Amicus" = "blue", "Amicus" = "red")) +
  coord_cartesian(ylim = c(0, 1)) +
  scale_y_continuous(
    breaks = seq(0, 1, by = 0.1),
    minor_breaks = seq(0, 1, by = 0.05)
  ) +
  labs(
    title = wrap_plot_text("Figure 1. Petitioner Vote Share by SG Amicus Status and Chief Justice", 70),
    subtitle = wrap_plot_text("Bar heights show the observed proportion of votes for the petitioner among Burger, Rehnquist, and Roberts.", 95),
    x = "Solicitor General Amicus (sgpetac)",
    y = "Proportion Voting for Petitioner",
    fill = "",
    caption = wrap_plot_text("Notes: Figure reports observed (unmodeled) petitioner-vote shares by SG amicus participation status for the three chief justices.", 120)
  ) +
  hw3_plot_theme

# Showing Figure 1 in the Plots pane when running the script.
print(p1)

# Saving Figure 1 with required dimensions/DPI.
# Saving the figure to disk with the specified dimensions.
ggsave("HW3 Fig1.png", plot = p1, width = 8.5, height = 6.5, dpi = 300)

# For Figure 2, keeping the same justices and adding pitch and term fields.
fig2_data <- justice_data %>%
  filter(justiceName %in% c("WEBurger", "WHRehnquist", "JGRoberts")) %>%
  select(justiceName, petitioner_vote, pitch_diff, term) %>%
  drop_na()

# Recomputing pitch grouping and period labels specifically for Figure 2.
fig2_mean <- mean(fig2_data$pitch_diff, na.rm = TRUE)
fig2_data <- fig2_data %>%
  mutate(
    high_pitch_diff = ifelse(
      pitch_diff > fig2_mean,
      "Above Avg. Pitch Differential",
      "Below Avg. Pitch Differential"
    ),
    high_pitch_diff = factor(
      high_pitch_diff,
      levels = c("Below Avg. Pitch Differential", "Above Avg. Pitch Differential")
    ),
    court_period = build_court_period(term),
    court_period = factor(court_period, levels = c("Burger", "Rehnquist", "Roberts"))
  )

# Calculating petitioner-vote share by court period and pitch group.
fig2_summary <- fig2_data %>%
  group_by(court_period, high_pitch_diff) %>%
  summarise(prop_petitioner_vote = mean(petitioner_vote), .groups = "drop")

# Building Figure 2 bar chart with assignment labels/colors.
# Creating the ggplot object and storing it in p2.
p2 <- ggplot(fig2_summary, aes(x = high_pitch_diff, y = prop_petitioner_vote, fill = high_pitch_diff)) +
  geom_col() +
  facet_wrap(~ court_period) +
  # Shortening x-axis tick labels so they do not overlap across facets.
  scale_x_discrete(labels = c(
    "Below Avg. Pitch Differential" = "Below Avg.",
    "Above Avg. Pitch Differential" = "Above Avg."
  )) +
  scale_fill_manual(values = c(
    "Below Avg. Pitch Differential" = "blue",
    "Above Avg. Pitch Differential" = "red"
  )) +
  coord_cartesian(ylim = c(0, 1)) +
  scale_y_continuous(
    breaks = seq(0, 1, by = 0.1),
    minor_breaks = seq(0, 1, by = 0.05)
  ) +
  labs(
    title = wrap_plot_text("Figure 2. Petitioner Vote Share by Pitch Differential Group and Court Period", 70),
    subtitle = wrap_plot_text("Pitch differential is split at the sample mean; bars show observed petitioner-vote shares within each court period.", 95),
    x = "Pitch Differential Group",
    y = "Proportion Voting for Petitioner",
    fill = "",
    caption = wrap_plot_text(paste(
      "Notes: Figure reports observed (unmodeled) petitioner-vote shares for below-average vs above-average pitch differential groups.",
      court_period_year_note
    ), 120)
  ) +
  hw3_plot_theme +
  theme(axis.text.x = element_text(angle = 15, hjust = 1))

# Showing Figure 2 in the Plots pane when running the script.
print(p2)

# Saving Figure 2 with required dimensions/DPI.
# Saving the figure to disk with the specified dimensions.
ggsave("HW3 Fig2.png", plot = p2, width = 8.5, height = 6.5, dpi = 300)

# ---------------------------
# 4) Section 3.3 Regression Analyses
# ---------------------------

# Setting up regression-ready dataset and core derived predictor.
analysis_data <- justice_data %>%
  mutate(
    pr_petitioner_pos = if_else(
      petitioner_wc > 0 & respondent_wc > 0,
      (petitioner_harvard_pos / petitioner_wc) - (respondent_harvard_pos / respondent_wc),
      NA_real_
    ),
    court_period = factor(build_court_period(term), levels = c("Burger", "Rehnquist", "Roberts"))
  )

# Running the Table 1 model sequence: baseline first, then justice controls, then justice plus term controls.
# Running linear model and storing result in m3_1.
m3_1 <- lm(petitioner_vote ~ pitch_diff + pr_petitioner_pos, data = analysis_data)
# Running linear model and storing result in m3_2.
m3_2 <- lm(petitioner_vote ~ pitch_diff + pr_petitioner_pos + factor(justiceName), data = analysis_data)
# Running linear model and storing result in m3_3.
m3_3 <- lm(petitioner_vote ~ pitch_diff + pr_petitioner_pos + factor(justiceName) + factor(term), data = analysis_data)

# Saving Table 1 in HTML format for easy Word paste.
stargazer(m3_1, m3_2, m3_3, type = "html", out = "HW3 Table1.html")

# Running pitch-by-court-period interaction model used for Figure 3.
# Running linear model and storing result in m3_period_base.
m3_period_base <- lm(petitioner_vote ~ pitch_diff + pr_petitioner_pos, data = analysis_data)
# Running linear model and storing result in m3_period_int.
m3_period_int <- lm(petitioner_vote ~ pitch_diff * court_period + pr_petitioner_pos, data = analysis_data)

# Creating a prediction grid for smooth interaction lines in Figure 3.
m3_period_frame <- model.frame(m3_period_int)
grid3 <- expand.grid(
  pitch_diff = seq(min(m3_period_frame$pitch_diff), max(m3_period_frame$pitch_diff), length.out = 120),
  court_period = levels(m3_period_frame$court_period),
  pr_petitioner_pos = mean(m3_period_frame$pr_petitioner_pos)
)
grid3$pred <- predict(m3_period_int, newdata = grid3)

# Showing predicted petitioner-vote probability across pitch by period.
# Creating the ggplot object and storing it in p3.
p3 <- ggplot(grid3, aes(x = pitch_diff, y = pred, color = court_period)) +
  geom_line(linewidth = 0.9) +
  scale_x_continuous(
    breaks = seq_axis_breaks(grid3$pitch_diff, by = 2.5),
    minor_breaks = seq_axis_breaks(grid3$pitch_diff, by = 1.25)
  ) +
  scale_y_continuous(
    breaks = seq_axis_breaks(grid3$pred, by = 0.25),
    minor_breaks = seq_axis_breaks(grid3$pred, by = 0.125)
  ) +
  labs(
    title = wrap_plot_text("Figure 3. Predicted Petitioner Vote Probability by Pitch Differential and Court Period", 70),
    subtitle = wrap_plot_text("Predictions from interaction model: petitioner_vote ~ pitch_diff * court_period + pr_petitioner_pos.", 95),
    x = "Pitch Differential",
    y = "Predicted Pr(Vote for Petitioner)",
    color = "Court Period",
    caption = wrap_plot_text(paste(
      "Notes: Lines show model-predicted values with pr_petitioner_pos held at its sample mean.",
      "This is the baseline court-period interaction specification used in Section 3.3.",
      court_period_year_note
    ), 120)
  ) +
  hw3_plot_theme

# Showing Figure 3 in the Plots pane when running the script.
print(p3)

# Saving Figure 3.
# Saving the figure to disk with the specified dimensions.
ggsave("HW3 Fig3.png", plot = p3, width = 8.5, height = 6.5, dpi = 300)

# Running the step-by-step model sequence used in Table 2.
# Running linear model and storing result in m_prog1.
m_prog1 <- lm(petitioner_vote ~ pitch_diff, data = analysis_data)
# Running linear model and storing result in m_prog2.
m_prog2 <- lm(petitioner_vote ~ pitch_diff + pr_petitioner_pos, data = analysis_data)
# Running linear model and storing result in m_prog3.
m_prog3 <- lm(petitioner_vote ~ pitch_diff + pr_petitioner_pos + sgpetac, data = analysis_data)
# Running linear model and storing result in m_prog4.
m_prog4 <- lm(petitioner_vote ~ pitch_diff + pr_petitioner_pos + sgpetac + court_period, data = analysis_data)
# Running linear model and storing result in m_prog5.
m_prog5 <- lm(petitioner_vote ~ pitch_diff * court_period + pr_petitioner_pos + sgpetac, data = analysis_data)
# Running linear model and storing result in m_prog6.
m_prog6 <- lm(petitioner_vote ~ pitch_diff * pr_petitioner_pos + sgpetac + court_period, data = analysis_data)

# Saving Table 2 with models 1 through 6.
stargazer(
  m_prog1, m_prog2, m_prog3, m_prog4, m_prog5, m_prog6,
  type = "html",
  out = "HW3 Table2.html"
)

# Creating a prediction grid for Figure 4 (pitch x court period interaction).
prog5_frame <- model.frame(m_prog5)
grid4 <- expand.grid(
  pitch_diff = seq(min(prog5_frame$pitch_diff), max(prog5_frame$pitch_diff), length.out = 120),
  court_period = levels(prog5_frame$court_period),
  pr_petitioner_pos = mean(prog5_frame$pr_petitioner_pos),
  sgpetac = mean(prog5_frame$sgpetac)
)
grid4$pred <- predict(m_prog5, newdata = grid4)

# Showing Figure 4 from Model 5 predictions.
# Creating the ggplot object and storing it in p4.
p4 <- ggplot(grid4, aes(x = pitch_diff, y = pred, color = court_period)) +
  geom_line(linewidth = 0.9) +
  scale_x_continuous(
    breaks = seq_axis_breaks(grid4$pitch_diff, by = 2.5),
    minor_breaks = seq_axis_breaks(grid4$pitch_diff, by = 1.25)
  ) +
  scale_y_continuous(
    breaks = seq_axis_breaks(grid4$pred, by = 0.25),
    minor_breaks = seq_axis_breaks(grid4$pred, by = 0.125)
  ) +
  labs(
    title = wrap_plot_text("Figure 4. Predicted Petitioner Vote Probability by Pitch Differential and Court Period (Model 5)", 70),
    subtitle = wrap_plot_text("Predictions from progressive Model 5: petitioner_vote ~ pitch_diff * court_period + pr_petitioner_pos + sgpetac.", 95),
    x = "Pitch Differential",
    y = "Predicted Pr(Vote for Petitioner)",
    color = "Court Period",
    caption = wrap_plot_text(paste(
      "Notes: Lines show Model 5 predictions with pr_petitioner_pos and sgpetac held at their sample means.",
      "Figure 4 differs from Figure 3 by adding sgpetac to the specification.",
      court_period_year_note
    ), 120)
  ) +
  hw3_plot_theme

# Showing Figure 4 in the Plots pane when running the script.
print(p4)

# Saving Figure 4.
# Saving the figure to disk with the specified dimensions.
ggsave("HW3 Fig4.png", plot = p4, width = 8.5, height = 6.5, dpi = 300)

# Creating a prediction grid for Figure 5 (pitch x pr_petitioner_pos interaction).
prog6_frame <- model.frame(m_prog6)
ref_period <- first_mode(prog6_frame$court_period)
pr_levels <- c(-2, -1, 0, 1, 2)

grid5 <- expand.grid(
  pitch_diff = seq(min(prog6_frame$pitch_diff), max(prog6_frame$pitch_diff), length.out = 120),
  pr_petitioner_pos = pr_levels,
  sgpetac = mean(prog6_frame$sgpetac),
  court_period = ref_period
)
grid5$pred <- predict(m_prog6, newdata = grid5)
grid5$pr_petitioner_pos <- factor(grid5$pr_petitioner_pos, levels = pr_levels)

# Showing Figure 5 using representative values of pr_petitioner_pos.
# Creating the ggplot object and storing it in p5.
p5 <- ggplot(grid5, aes(x = pitch_diff, y = pred, color = pr_petitioner_pos)) +
  geom_line(linewidth = 0.9) +
  scale_x_continuous(
    breaks = seq_axis_breaks(grid5$pitch_diff, by = 2.5),
    minor_breaks = seq_axis_breaks(grid5$pitch_diff, by = 1.25)
  ) +
  scale_y_continuous(
    breaks = pretty(grid5$pred, n = 8),
    minor_breaks = pretty(grid5$pred, n = 16)
  ) +
  labs(
    title = wrap_plot_text("Figure 5. Predicted Petitioner Vote Probability by Pitch Differential and Petitioner Positivity", 70),
    x = "Pitch Differential",
    y = "Predicted Pr(Vote for Petitioner)",
    color = "pr_petitioner_pos",
    subtitle = wrap_plot_text(paste(
      "Predictions from progressive Model 6 with pitch_diff * pr_petitioner_pos interaction.",
      "Court period held at:",
      ref_period
    ), 95),
    caption = wrap_plot_text(paste(
      "Notes: Lines show Model 6 predictions evaluated at representative pr_petitioner_pos values (-2, -1, 0, 1, 2),",
      "with sgpetac held at its sample mean and court period fixed at the modal category.",
      court_period_year_note
    ), 120)
  ) +
  hw3_plot_theme

# Showing Figure 5 in the Plots pane when running the script.
print(p5)

# Saving Figure 5.
# Saving the figure to disk with the specified dimensions.
ggsave("HW3 Fig5.png", plot = p5, width = 8.5, height = 6.5, dpi = 300)

# ---------------------------
# 5) Section 3.4 Outlier Analysis and Validity
# ---------------------------

# Using progressive Model 6 as the final model for outlier diagnostics.
final_model <- m_prog6
# Calculating assignment-required influence diagnostics.
stud_resid <- rstudent(final_model)
leverage <- hatvalues(final_model)
cooks_d <- cooks.distance(final_model)
dffits_val <- dffits(final_model)

# Building one diagnostics table per model row.
outlier_df <- data.frame(
  obs_id = seq_along(stud_resid),
  studentized_resid = stud_resid,
  leverage = leverage,
  cooks_d = cooks_d,
  dffits = dffits_val
)

# Calculating cutoffs from assignment formulas.
n_model <- nrow(model.frame(final_model))
k_model <- length(coef(final_model)) - 1
thr_resid <- 2
thr_lev <- (2 * k_model + 2) / n_model
thr_cook <- 4 / n_model
thr_dffits <- 2 * sqrt(k_model / n_model)

# Flagging rows crossing any threshold and rows crossing all thresholds.
outlier_df <- outlier_df %>%
  dplyr::mutate(
    is_outlier = abs(studentized_resid) > thr_resid |
      leverage > thr_lev |
      cooks_d > thr_cook |
      abs(dffits) > thr_dffits,
    is_egregious = abs(studentized_resid) > thr_resid &
      leverage > thr_lev &
      cooks_d > thr_cook &
      abs(dffits) > thr_dffits,
    abs_dffits = abs(dffits)
  )

# Showing leverage vs |DFFITS| with threshold lines.
# Creating the ggplot object and storing it in p6.
p6 <- ggplot(outlier_df, aes(x = abs_dffits, y = leverage, color = is_outlier)) +
  geom_point(alpha = 0.75) +
  geom_hline(yintercept = thr_lev, linetype = "dashed", color = "blue") +
  geom_vline(xintercept = thr_dffits, linetype = "dashed", color = "red") +
  geom_text(
    data = subset(outlier_df, is_egregious),
    aes(label = obs_id),
    vjust = -0.4,
    size = 2.8,
    check_overlap = TRUE
  ) +
  scale_color_manual(values = c("FALSE" = "black", "TRUE" = "red")) +
  scale_x_continuous(
    breaks = pretty(outlier_df$abs_dffits, n = 10),
    minor_breaks = pretty(outlier_df$abs_dffits, n = 20)
  ) +
  scale_y_continuous(
    breaks = pretty(outlier_df$leverage, n = 10),
    minor_breaks = pretty(outlier_df$leverage, n = 20)
  ) +
  labs(
    title = wrap_plot_text("Figure 6. Influence Diagnostics: Leverage vs |DFFITS|", 70),
    subtitle = wrap_plot_text("Outlier screening for the final regression model; dashed lines mark thresholds.", 95),
    x = "|DFFITS|",
    y = "Leverage",
    color = "Outlier",
    caption = wrap_plot_text("Notes: Points are flagged as outliers when any threshold is exceeded (studentized residual, leverage, Cook's D, or |DFFITS|). Labels mark observations exceeding all thresholds.", 120)
  ) +
  hw3_plot_theme

# Showing Figure 6 in the Plots pane when running the script.
print(p6)

# Saving Figure 6.
# Saving the figure to disk with the specified dimensions.
ggsave("HW3 Fig6.png", plot = p6, width = 8.5, height = 6.5, dpi = 300)

# Aligning analysis_data rows to the exact estimation sample used in final_model.
model_rows <- as.integer(rownames(model.frame(final_model)))
analysis_data_used <- analysis_data[model_rows, ]
# Removing flagged outliers for robustness comparison model.
clean_data <- analysis_data_used[!outlier_df$is_outlier, ]

# Running final specification on full sample and outlier-excluded sample.
model_full <- lm(
  petitioner_vote ~ pitch_diff * pr_petitioner_pos + sgpetac + court_period,
  data = analysis_data_used
)
model_clean <- lm(
  petitioner_vote ~ pitch_diff * pr_petitioner_pos + sgpetac + court_period,
  data = clean_data
)

# Saving full-vs-clean comparison table (Table 3) as HTML.
stargazer(model_full, model_clean, type = "html", out = "HW3 Table3.html")

# Saving a short diagnostics summary so it is easy to cite in the write-up.
outlier_summary <- c(
  "Outlier Summary (Section 3.4)",
  paste("Model observations:", n_model),
  paste("k (predictors):", k_model),
  paste("Threshold |studentized residual| >", thr_resid),
  paste("Threshold leverage >", round(thr_lev, 6)),
  paste("Threshold Cook's D >", round(thr_cook, 6)),
  paste("Threshold |DFFITS| >", round(thr_dffits, 6)),
  paste("Flagged outliers (any threshold):", sum(outlier_df$is_outlier)),
  paste("Flagged egregious outliers (all thresholds):", sum(outlier_df$is_egregious))
)
write_html_pre(outlier_summary, "HW3_OutlierSummary.html", "HW3 Outlier Summary")
