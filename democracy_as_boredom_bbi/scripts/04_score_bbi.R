suppressPackageStartupMessages({
  library(dplyr)
  library(purrr)
  library(readr)
  library(stringr)
})

clean <- readr::read_csv("data_clean/presidential_speeches_clean.csv", show_col_types = FALSE)
dict <- readr::read_csv("dictionaries/bbi_dictionary.csv", show_col_types = FALSE)

count_terms <- function(text, terms) {
  sum(map_int(terms, function(term) {
    pattern <- paste0("\\b", str_replace_all(str_to_lower(term), "([\\W])", "\\\\\\1"), "\\b")
    str_count(text, regex(pattern, ignore_case = TRUE))
  }))
}

procedural_terms <- dict |> filter(category == "procedural_constraint") |> pull(term)
charismatic_terms <- dict |> filter(category == "charismatic_sovereignty") |> pull(term)

z_safe <- function(x) {
  if (sd(x, na.rm = TRUE) == 0) return(rep(0, length(x)))
  as.numeric(scale(x))
}

scored <- clean |>
  mutate(
    procedural_term_count = map_int(text_lower, count_terms, procedural_terms),
    charismatic_term_count = map_int(text_lower, count_terms, charismatic_terms),
    procedural_terms_per_1000_words = procedural_term_count / word_count * 1000,
    charismatic_terms_per_1000_words = charismatic_term_count / word_count * 1000,
    procedural_z_score = z_safe(procedural_terms_per_1000_words),
    charismatic_z_score = z_safe(charismatic_terms_per_1000_words),
    BBI_raw = procedural_z_score - charismatic_z_score,
    BBI_z = BBI_raw,
    BBI_ratio = (procedural_terms_per_1000_words + 0.1) / (charismatic_terms_per_1000_words + 0.1),
    BBI_net_raw = procedural_terms_per_1000_words - charismatic_terms_per_1000_words
  )

readr::write_csv(scored, "data_clean/presidential_speeches_bbi_scored.csv")
