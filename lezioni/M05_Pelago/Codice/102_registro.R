dir.create("Risultati",
           showWarnings = FALSE)
registro102 <- list(
  n = 30, B = 200, seed = 17,
  unita = "osservazione",
  statistica = "media",
  quantili = "type 7",
  ambiente = sessionInfo())
saveRDS(registro102,
        "Risultati/registro.rds")
