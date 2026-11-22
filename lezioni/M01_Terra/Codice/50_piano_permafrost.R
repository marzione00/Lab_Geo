# Piano didattico, senza misure reali
piano <- data.frame(
  sito = rep(1:8, each = 5),
  anno = rep(2020:2024, times = 8))
# Numero di righe per sito e anno
with(piano, table(sito, anno))
