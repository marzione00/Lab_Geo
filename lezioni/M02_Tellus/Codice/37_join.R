# Tabelle costruite nella slide 34
uniti <- merge(provini, siti,
  by = "sito", all.x = TRUE)
# Ogni provino deve restare presente
stopifnot(nrow(uniti) ==
          nrow(provini))
uniti
