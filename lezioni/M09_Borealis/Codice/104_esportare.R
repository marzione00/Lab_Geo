dir.create("Risultati", showWarnings = FALSE)
write.csv(confronto,
  "Risultati/CO2_trasformazioni.csv",
  row.names = FALSE)
scelte <- list(periodo = range(d$data),
  frequenza = 12, ritardi = c(1, 12),
  ADF_k = 4, KPSS_lshort = TRUE)
saveRDS(scelte, "Risultati/scelte.rds")
