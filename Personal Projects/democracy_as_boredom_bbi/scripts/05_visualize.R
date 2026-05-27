suppressPackageStartupMessages({
  library(dplyr)
  library(forcats)
  library(ggplot2)
  library(readr)
  library(stringr)
})

dir.create("outputs/figures", showWarnings = FALSE, recursive = TRUE)

scored <- readr::read_csv("data_clean/presidential_speeches_bbi_scored.csv", show_col_types = FALSE)

save_plot <- function(plot, name, width = 9, height = 6) {
  ggsave(file.path("outputs/figures", paste0(name, ".png")), plot, width = width, height = height, dpi = 300)
  ggsave(file.path("outputs/figures", paste0(name, ".pdf")), plot, width = width, height = height)
}

theme_bbi <- theme_minimal(base_size = 12) +
  theme(plot.title = element_text(face = "bold"), panel.grid.minor = element_blank())

p1 <- scored |>
  filter(!is.na(year)) |>
  ggplot(aes(year, BBI_z, color = speech_type)) +
  geom_hline(yintercept = 0, color = "gray70") +
  geom_point(alpha = 0.55) +
  geom_smooth(se = FALSE, method = "loess", formula = y ~ x) +
  labs(title = "Bureaucratic Boredom Index over time", x = "Year", y = "BBI z-score", color = "Speech type",
       caption = "Source: American Presidency Project; dictionary scores per 1,000 words.") +
  theme_bbi
save_plot(p1, "01_bbi_over_time")

p2 <- scored |>
  group_by(president) |>
  summarize(mean_bbi = mean(BBI_z, na.rm = TRUE), n = n(), .groups = "drop") |>
  mutate(president = as.character(president)) |>
  filter(!is.na(president), president != "", n >= 1) |>
  arrange(mean_bbi) |>
  mutate(president = fct_reorder(president, mean_bbi)) |>
  ggplot(aes(mean_bbi, president)) +
  geom_col(fill = "#3a6ea5") +
  labs(title = "Average BBI by president", x = "Mean BBI z-score", y = NULL,
       caption = "Includes available inaugural and State of the Union category documents.") +
  theme_bbi
save_plot(p2, "02_average_bbi_by_president", width = 9, height = 10)

p3 <- scored |>
  filter(!is.na(year)) |>
  ggplot(aes(year, procedural_terms_per_1000_words, color = speech_type)) +
  geom_point(alpha = 0.55) +
  geom_smooth(se = FALSE, method = "loess", formula = y ~ x) +
  labs(title = "Procedural constraint language over time", x = "Year", y = "Procedural terms per 1,000 words", color = "Speech type") +
  theme_bbi
save_plot(p3, "03_procedural_score_over_time")

p4 <- scored |>
  filter(!is.na(year)) |>
  ggplot(aes(year, charismatic_terms_per_1000_words, color = speech_type)) +
  geom_point(alpha = 0.55) +
  geom_smooth(se = FALSE, method = "loess", formula = y ~ x) +
  labs(title = "Charismatic sovereignty language over time", x = "Year", y = "Charismatic terms per 1,000 words", color = "Speech type") +
  theme_bbi
save_plot(p4, "04_charismatic_score_over_time")

p5 <- scored |>
  ggplot(aes(speech_type, BBI_z, fill = speech_type)) +
  geom_boxplot(alpha = 0.8, show.legend = FALSE) +
  labs(title = "BBI by speech type", x = NULL, y = "BBI z-score") +
  theme_bbi
save_plot(p5, "05_bbi_by_speech_type")

top_high <- scored |> slice_max(BBI_z, n = 10, with_ties = FALSE) |> mutate(label = str_trunc(paste(year, president, title), 55))
p6 <- top_high |>
  mutate(label = fct_reorder(label, BBI_z)) |>
  ggplot(aes(BBI_z, label)) +
  geom_col(fill = "#4b8f5a") +
  labs(title = "Top 10 highest-BBI speeches", x = "BBI z-score", y = NULL) +
  theme_bbi
save_plot(p6, "06_top_10_highest_bbi", width = 10, height = 6)

top_low <- scored |> slice_min(BBI_z, n = 10, with_ties = FALSE) |> mutate(label = str_trunc(paste(year, president, title), 55))
p7 <- top_low |>
  mutate(label = fct_reorder(label, BBI_z)) |>
  ggplot(aes(BBI_z, label)) +
  geom_col(fill = "#b8584f") +
  labs(title = "Top 10 lowest-BBI speeches", x = "BBI z-score", y = NULL) +
  theme_bbi
save_plot(p7, "07_top_10_lowest_bbi", width = 10, height = 6)

p8 <- scored |>
  ggplot(aes(BBI_z)) +
  geom_histogram(bins = 30, fill = "#6c7a89", color = "white") +
  labs(title = "Distribution of BBI scores", x = "BBI z-score", y = "Speech count") +
  theme_bbi
save_plot(p8, "08_bbi_distribution")

p9 <- scored |>
  ggplot(aes(procedural_terms_per_1000_words, charismatic_terms_per_1000_words, color = speech_type)) +
  geom_point(alpha = 0.7) +
  labs(title = "Procedural versus charismatic language", x = "Procedural terms per 1,000 words", y = "Charismatic terms per 1,000 words", color = "Speech type") +
  theme_bbi
save_plot(p9, "09_procedural_vs_charismatic")
