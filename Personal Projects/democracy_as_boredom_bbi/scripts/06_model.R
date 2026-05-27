suppressPackageStartupMessages({
  library(broom)
  library(dplyr)
  library(modelsummary)
  library(readr)
})

dir.create("outputs/tables", showWarnings = FALSE, recursive = TRUE)

scored <- readr::read_csv("data_clean/presidential_speeches_bbi_scored.csv", show_col_types = FALSE) |>
  filter(!is.na(year), !is.na(president), !is.na(speech_type))

m1 <- lm(BBI_z ~ year + speech_type, data = scored)
m2 <- if (n_distinct(scored$president) > 1) {
  lm(BBI_z ~ president + speech_type, data = scored)
} else {
  lm(BBI_z ~ speech_type, data = scored)
}
m3_data <- scored |>
  filter(!is.na(divided_government), !is.na(major_war_period), !is.na(recession_indicator))
m3 <- if (nrow(m3_data) >= 20) {
  lm(BBI_z ~ divided_government + major_war_period + recession_indicator + speech_type, data = m3_data)
} else {
  lm(BBI_z ~ speech_type, data = scored)
}
m4a <- lm(procedural_terms_per_1000_words ~ year + speech_type, data = scored)
m4b <- lm(charismatic_terms_per_1000_words ~ year + speech_type, data = scored)

models <- list(
  "BBI: year and speech type" = m1,
  "BBI: president and speech type" = m2,
  "BBI: government control and crisis" = m3,
  "Procedural score" = m4a,
  "Charismatic score" = m4b
)

modelsummary::modelsummary(
  models,
  output = "outputs/tables/preliminary_models.html",
  statistic = "std.error",
  stars = TRUE,
  notes = "Model 3 uses divided government, major-war, and recession indicators when available. GDP is exported for later model specifications but not included here because coverage begins in 1947."
)

tidied <- bind_rows(
  tidy(m1) |> mutate(model = "model_1_bbi_year_type"),
  tidy(m2) |> mutate(model = "model_2_bbi_president_type"),
  tidy(m3) |> mutate(model = "model_3_bbi_control_crisis"),
  tidy(m4a) |> mutate(model = "model_4a_procedural_year_type"),
  tidy(m4b) |> mutate(model = "model_4b_charismatic_year_type")
)
readr::write_csv(tidied, "outputs/tables/preliminary_models_tidy.csv")

summary_stats <- scored |>
  summarize(
    speeches = n(),
    first_year = min(year, na.rm = TRUE),
    last_year = max(year, na.rm = TRUE),
    mean_bbi = mean(BBI_z, na.rm = TRUE),
    sd_bbi = sd(BBI_z, na.rm = TRUE),
    mean_procedural_per_1000 = mean(procedural_terms_per_1000_words, na.rm = TRUE),
    mean_charismatic_per_1000 = mean(charismatic_terms_per_1000_words, na.rm = TRUE),
    party_nonmissing = sum(!is.na(party)),
    divided_government_nonmissing = sum(!is.na(divided_government)),
    recession_indicator_nonmissing = sum(!is.na(recession_indicator)),
    gdp_nonmissing = sum(!is.na(gdp_billions_current_dollars)),
    major_war_period_nonmissing = sum(!is.na(major_war_period))
  )
readr::write_csv(summary_stats, "outputs/tables/summary_statistics.csv")
