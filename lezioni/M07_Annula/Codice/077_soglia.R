# Probabilita' descrittive gia' calcolate.
soglia77 <- 0.5
classe77 <- as.integer(p_log >= soglia77)
head(data.frame(
  probabilita = p_log,
  classe = classe77,
  osservato = f$spiky))
