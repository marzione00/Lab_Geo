# Sintesi per stazione di Terra01.
risultato <- aggregate(
  valore ~ stazione, terra, mean)
dir.create("Risultati",
           showWarnings = FALSE)
write.csv(risultato,
  "Risultati/medie_stazioni.csv",
  row.names = FALSE)
sessionInfo()          # versioni di R
