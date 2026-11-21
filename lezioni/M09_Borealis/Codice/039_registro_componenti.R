tab_T <- data.frame(
  data = temp$data,
  osservata = temp$temperatura_C,
  riferimento = riferimento_T,
  anomalia = anomalia_T,
  resto_STL = componenti_T[, "remainder"])
head(tab_T, 3)
