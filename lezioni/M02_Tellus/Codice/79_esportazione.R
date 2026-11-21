dir.create("Risultati",
           showWarnings = FALSE)
percorso_tab <- file.path("Risultati",
  "fossili_analitici.csv")
write.csv(analitica, percorso_tab,
  row.names = FALSE, na = "NA")
write.csv(registro,
  "Risultati/registro_controlli.csv",
  row.names = FALSE, na = "NA")
