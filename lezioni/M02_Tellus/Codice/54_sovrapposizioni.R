nomi_flag <- c("misura_mancante",
  "non_positivo", "interno_superiore")
flags <- fossili[nomi_flag]
colSums(flags) # 2, 1, 2
coinvolte <- rowSums(flags) > 0
sum(coinvolte) # 4 righe
