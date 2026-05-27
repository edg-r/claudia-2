suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
  library(tibble)
})

dir.create("dictionaries", showWarnings = FALSE, recursive = TRUE)

procedural <- c(
  "law", "legal", "constitution", "constitutional", "court", "courts",
  "congress", "committee", "committees", "hearing", "hearings", "statute",
  "statutory", "implementation", "implement", "implemented", "regulation",
  "regulatory", "budget", "budgets", "appropriation", "appropriations",
  "oversight", "audit", "audits", "report", "reports", "review", "agency",
  "agencies", "federal", "state", "local", "program", "programs",
  "pilot program", "evaluation", "compliance", "consultation", "stakeholder",
  "stakeholders", "bipartisan", "amendment", "authorization", "interagency",
  "administration", "administrative", "department", "departments",
  "legislation", "legislative", "executive order", "rules", "rulemaking",
  "governor", "governors", "mayor", "mayors", "grant", "grants"
)

charismatic <- c(
  "destiny", "rebirth", "greatness", "great", "betrayal", "betray",
  "enemy", "enemies", "traitor", "traitors", "sacrifice", "sacrifices",
  "glory", "humiliation", "humiliated", "corrupt", "corruption", "pure",
  "purity", "strength", "strong", "weakness", "weak", "crisis", "invasion",
  "threat", "threats", "restore", "restoration", "save", "saved",
  "movement", "loyalty", "loyal", "will of the people", "the people",
  "national will", "enemies within", "foreign enemies", "betrayed",
  "disaster", "disgrace", "forgotten", "salvation", "revival", "great again"
)

make_dict <- function(terms, category, rationale) {
  tibble(term = terms) |>
    mutate(
      category = category,
      term_type = case_when(
        str_count(term, "\\S+") == 1 ~ "unigram",
        str_count(term, "\\S+") == 2 ~ "bigram",
        TRUE ~ "phrase"
      ),
      notes = "Initial transparent dictionary term",
      theoretical_rationale = rationale
    )
}

dict <- bind_rows(
  make_dict(procedural, "procedural_constraint", "Signals legal, legislative, administrative, budgetary, oversight, or implementation constraint."),
  make_dict(charismatic, "charismatic_sovereignty", "Signals destiny, crisis, people-as-one, enemy construction, personalism, restoration, or existential rhetoric.")
) |>
  distinct(term, category, .keep_all = TRUE)

readr::write_csv(dict, "dictionaries/bbi_dictionary.csv")
