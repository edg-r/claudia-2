################################################################################
# Homework 2 Part II: Regression Discontinuity Design
################################################################################

# This script answers Questions 5-9. It uses the grade5 dataset to show the
# first-stage class-size jump at Maimonides' Rule and estimate local RD effects
# on math and verbal scores around the enrollment cutoff of 40.

################################################################################
# Setup & Output Folders
################################################################################

options(stringsAsFactors = FALSE)

# Locate the homework folder whether the script is run from RStudio or terminal.
args_file <- commandArgs(trailingOnly = FALSE)
script_arg <- grep("^--file=", args_file, value = TRUE)
part_dir <- if (length(script_arg) > 0) {
  dirname(normalizePath(sub("^--file=", "", script_arg[1])))
} else {
  getwd()
}
setwd(part_dir)

out_dir <- file.path(part_dir, "outputs", "part_ii")
lib_dir <- file.path(out_dir, "R_libs")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(lib_dir, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(normalizePath(lib_dir), .libPaths()))

needed <- c("haven", "ggplot2")
missing_needed <- needed[!vapply(needed, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing_needed) > 0) {
  stop("Missing required package(s): ", paste(missing_needed, collapse = ", "))
}

library(haven)
library(ggplot2)

# Main RD choices used throughout the script.
cutoff <- 40
max_enrollment <- 80
manual_bw <- 10

################################################################################
# Load Data and Record Schema
################################################################################

# Read the Stata file and export a schema so variable labels/ranges are easy to
# check without re-opening the raw data.
grade5 <- read_dta("grade5.dta")
core_vars <- c("schlcode", "school_enrollment", "classize", "avgmath",
               "avgverb", "disadvantaged", "female", "religious")

schema <- data.frame(
  variable = names(grade5),
  class = vapply(grade5, function(x) paste(class(x), collapse = "/"), character(1)),
  label = vapply(grade5, function(x) {
    label <- attr(x, "label", exact = TRUE)
    if (is.null(label)) "" else as.character(label)
  }, character(1)),
  n_missing = vapply(grade5, function(x) sum(is.na(x)), integer(1)),
  min = vapply(grade5, function(x) if (is.numeric(x)) min(x, na.rm = TRUE) else NA_real_, numeric(1)),
  max = vapply(grade5, function(x) if (is.numeric(x)) max(x, na.rm = TRUE) else NA_real_, numeric(1))
)
write.csv(schema, file.path(out_dir, "grade5_schema.csv"), row.names = FALSE)

# Create the centered running variable and treatment indicator for crossing 40.
analysis <- grade5[, core_vars]
analysis$enrollment_centered <- analysis$school_enrollment - cutoff
analysis$above_cutoff <- as.integer(analysis$school_enrollment >= cutoff)
analysis_under80 <- subset(analysis, school_enrollment < max_enrollment)

################################################################################
# Q6: Histogram of the Running Variable
################################################################################

# If families manipulate school choice around the rule, we would expect suspicious
# bunching near 40. The histogram is a visual check for that.
png(file.path(out_dir, "hist_school_enrollment.png"), width = 1600, height = 1000, res = 180)
print(
  ggplot(analysis, aes(x = school_enrollment)) +
    geom_histogram(binwidth = 5, boundary = 0, color = "white", fill = "#4C78A8") +
    geom_vline(xintercept = cutoff, color = "#C44E52", linewidth = 1) +
    labs(
      title = "Distribution of Fifth-Grade School Enrollment",
      subtitle = "Vertical line marks the Maimonides Rule cutoff at 40 students",
      x = "School enrollment",
      y = "Number of observations"
    ) +
    theme_minimal(base_size = 12)
)
dev.off()

################################################################################
# Q7: Relationship Between Class Size and Scores
################################################################################

# Plot the first stage and score outcomes near the cutoff. The binned points make
# the local pattern easier to see than raw overplotted observations alone.
make_rdd_plot <- function(y_var, y_label, file_name) {
  plot_data <- subset(analysis, school_enrollment < max_enrollment)
  bin_data <- aggregate(plot_data[[y_var]],
                        by = list(school_enrollment = plot_data$school_enrollment),
                        FUN = mean, na.rm = TRUE)
  names(bin_data)[2] <- "mean_outcome"

  png(file.path(out_dir, file_name), width = 1600, height = 1000, res = 180)
  print(
    ggplot(plot_data, aes(x = school_enrollment, y = .data[[y_var]])) +
      geom_point(alpha = 0.18, color = "#4D4D4D", size = 1.1) +
      geom_point(data = bin_data, aes(y = mean_outcome), color = "#1B9E77", size = 2) +
      geom_smooth(
        data = subset(plot_data, school_enrollment < cutoff),
        method = "lm", formula = y ~ x, se = TRUE, color = "#1F77B4"
      ) +
      geom_smooth(
        data = subset(plot_data, school_enrollment >= cutoff),
        method = "lm", formula = y ~ x, se = TRUE, color = "#D62728"
      ) +
      geom_vline(xintercept = cutoff, color = "#C44E52", linewidth = 1) +
      labs(
        title = paste(y_label, "Around the Enrollment Cutoff"),
        subtitle = "Schools with enrollment below 80; separate linear fits on each side of 40",
        x = "School enrollment",
        y = y_label
      ) +
      theme_minimal(base_size = 12)
  )
  dev.off()
}

make_rdd_plot("classize", "Class size", "rdd_classize_cutoff40.png")
make_rdd_plot("avgmath", "Average math score", "rdd_avgmath_cutoff40.png")
make_rdd_plot("avgverb", "Average verbal score", "rdd_avgverb_cutoff40.png")

################################################################################
# Q8a: Manual Local Linear RD
################################################################################

# Estimate separate slopes on the left and right of the cutoff. The coefficient
# on above_cutoff is the estimated jump exactly at 40.
manual_rd <- function(data, outcome, bw) {
  window <- subset(data, abs(school_enrollment - cutoff) <= bw)
  window <- window[!is.na(window[[outcome]]) &
                     !is.na(window$school_enrollment) &
                     !is.na(window$above_cutoff), ]
  fit <- lm(reformulate(c("above_cutoff", "enrollment_centered",
                          "above_cutoff:enrollment_centered"), outcome), data = window)
  coefs <- summary(fit)$coefficients
  left <- subset(window, school_enrollment < cutoff)
  right <- subset(window, school_enrollment >= cutoff)
  data.frame(
    outcome = outcome,
    cutoff = cutoff,
    bandwidth = bw,
    estimate = unname(coefs["above_cutoff", "Estimate"]),
    std_error = unname(coefs["above_cutoff", "Std. Error"]),
    p_value = unname(coefs["above_cutoff", "Pr(>|t|)"]),
    n_left = nrow(left),
    n_right = nrow(right),
    unique_schools_left = length(unique(left$schlcode)),
    unique_schools_right = length(unique(right$schlcode)),
    stringsAsFactors = FALSE
  )
}

manual_results <- rbind(
  manual_rd(analysis_under80, "avgmath", manual_bw),
  manual_rd(analysis_under80, "avgverb", manual_bw),
  manual_rd(analysis_under80, "classize", manual_bw),
  manual_rd(analysis_under80, "disadvantaged", manual_bw)
)
write.csv(manual_results, file.path(out_dir, "manual_local_linear_results.csv"), row.names = FALSE)

################################################################################
# Q8b: rdrobust RD Estimates
################################################################################

# Use rdrobust when available. If it is missing, write a blocker file rather than
# breaking the rest of the script.
rdrobust_blocker <- NULL
rdrobust_results <- data.frame()
if (!requireNamespace("rdrobust", quietly = TRUE)) {
  rdrobust_blocker <- paste0(
    "rdrobust package unavailable after checking .libPaths(): ",
    paste(.libPaths(), collapse = "; ")
  )
} else {
  rd_result <- function(outcome) {
    x <- analysis_under80$school_enrollment
    y <- analysis_under80[[outcome]]
    ok <- !is.na(x) & !is.na(y)
    obj <- rdrobust::rdrobust(y = y[ok], x = x[ok], c = cutoff)
    ci <- obj$ci
    coef <- obj$coef
    se <- obj$se
    data.frame(
      outcome = outcome,
      cutoff = cutoff,
      estimate_conventional = unname(coef[1, 1]),
      se_conventional = unname(se[1, 1]),
      ci95_low_conventional = unname(ci[1, 1]),
      ci95_high_conventional = unname(ci[1, 2]),
      bandwidth_left = unname(obj$bws[1, 1]),
      bandwidth_right = unname(obj$bws[1, 2]),
      n_left = unname(obj$N_h[1]),
      n_right = unname(obj$N_h[2]),
      stringsAsFactors = FALSE
    )
  }
  rdrobust_results <- rbind(rd_result("avgmath"), rd_result("avgverb"))
  write.csv(rdrobust_results, file.path(out_dir, "rdrobust_default_results.csv"), row.names = FALSE)
}

if (!is.null(rdrobust_blocker)) {
  writeLines(rdrobust_blocker, file.path(out_dir, "rdrobust_blocker.txt"))
}

################################################################################
# Q9: Falsification Test
################################################################################

# The smoothness check for disadvantaged uses the same manual RD function above.
# A jump here would warn that the cutoff changes student composition, not only
# class size. The row is already included in manual_results.

################################################################################
# Save Terminal Summary
################################################################################

# Write a compact text summary for quick debugging and final-report integration.
sink(file.path(out_dir, "summary_output.txt"))
cat("Homework 2 Part II RDD summary\n")
cat("Generated:", format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z"), "\n\n")
cat("Dataset dimensions:", nrow(grade5), "rows x", ncol(grade5), "columns\n")
cat("Unique schools:", length(unique(grade5$schlcode)), "\n")
cat("Manual local linear bandwidth:", manual_bw, "students around cutoff", cutoff, "\n")
cat("Manual results:\n")
print(manual_results)
cat("\nrdrobust results:\n")
if (nrow(rdrobust_results) > 0) {
  print(rdrobust_results)
} else {
  cat(rdrobust_blocker, "\n")
}
cat("\nInterpretation notes:\n")
cat("- Manual estimates use a local linear specification with different slopes on each side of 40.\n")
cat("- The disadvantaged covariate is the falsification/smoothness test.\n")
cat("- Positive outcome coefficient means observations just above 40 score higher than just below 40.\n")
cat("- For classize, crossing 40 should mechanically lower class size because a second class is opened.\n")
sink()

################################################################################
# Write Part II Notes
################################################################################

# Build the interpretation notes used by the final report. Keep the prose concise
# enough that Edgar can explain each line and each estimate.
notes <- c(
  "# Homework 2 Part II Notes",
  "",
  "## Source and Design",
  "",
  "Paper: Angrist, J. D., & Lavy, V. (1999). Using Maimonides' Rule to Estimate the Effect of Class Size on Scholastic Achievement. Quarterly Journal of Economics, 114(2), 533-575. https://doi.org/10.1162/003355399556061",
  "",
  "The local `rdd_paper.pdf` is a scan-only PDF, so direct text extraction returned blank pages. For the intro answer, use the paper metadata and abstract from the QJE/NBER pages together with the assignment-provided PDF. The intro frames the problem as a class-size causal inference problem: parents, teachers, and scholars care about class size, but ordinary observational comparisons can mix class-size effects with nonrandom school and family characteristics.",
  "",
  "Draft answer for Question 1: A simple OLS regression of test scores on class size is likely endogenous because class size is not randomly assigned. Schools with smaller classes may also differ in parental resources, neighborhood income, school quality, teacher quality, peer composition, religious status, and the share of disadvantaged students. If advantaged families sort into schools with smaller classes, OLS would make small classes look more beneficial than they truly are, so the class-size coefficient would be too negative. A competing bias is compensatory placement: schools may assign smaller classes to weaker or more disadvantaged students, which would make small classes look less beneficial. The most intuitive omitted-variable concern in this setting is family/school advantage, so I would expect naive OLS to overstate the benefit of small classes unless the data show strong compensatory assignment.",
  "",
  "## Question 2",
  "",
  "The histogram is saved as `outputs/part_ii/hist_school_enrollment.png`. There is no visually obvious bunching immediately below 40 in this data, so the histogram does not strongly suggest that parents choose schools strategically around Maimonides' Rule. If parents were manipulating enrollment to obtain smaller classes, we would expect suspicious piling up just above or below rule thresholds.",
  "",
  "## Question 3",
  "",
  "RDD plots are saved as `outputs/part_ii/rdd_classize_cutoff40.png`, `outputs/part_ii/rdd_avgmath_cutoff40.png`, and `outputs/part_ii/rdd_avgverb_cutoff40.png`. The class-size plot should show the first-stage drop at 40. The math and verbal plots show whether achievement jumps at the same cutoff; if scores rise where class size falls, that supports the smaller-class interpretation, but the evidence should be described as local to schools near 40 students.",
  "",
  "## Question 4 Manual Local Regression",
  "",
  "Manual estimates use schools/classes with enrollment below 80 and a bandwidth of 10 students around the 40-student cutoff. This bandwidth keeps the comparison local while retaining observations on both sides of the cutoff.",
  "",
  paste(capture.output(print(manual_results)), collapse = "\n"),
  "",
  "## Question 4 rdrobust",
  "",
  if (nrow(rdrobust_results) > 0) paste(capture.output(print(rdrobust_results)), collapse = "\n") else rdrobust_blocker,
  "",
  "## Question 5 Falsification Test",
  "",
  "I used covariate smoothness in `disadvantaged` as the falsification test. Because disadvantage is predetermined relative to the class-size rule, it should not jump discontinuously at 40 if observations just below and just above the cutoff are comparable. A meaningful discontinuity would imply that the RD estimate may be mixing class-size effects with a change in student composition.",
  "",
  paste(capture.output(print(subset(manual_results, outcome == "disadvantaged"))), collapse = "\n"),
  "",
  "---",
  "Generated for: Edgar Agunias",
  "Date: 2026-05-18",
  "Model: GPT-5 Codex",
  "Sources: `grade5.dta`, `Homework 2_ Panel & RDD.pdf`, local scan-only `rdd_paper.pdf`, QJE/NBER metadata for Angrist and Lavy (1999)",
  "Agent: Hephaestus assisting Tyche",
  "---"
)
writeLines(notes, "PART_II_NOTES.md")
