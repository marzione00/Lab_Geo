d <- data.frame(
  stazione = c("A", "A", "B", "B"),
  valore = c(3.1, NA, 7, 7))
# Numero di valori mancanti
sum(is.na(d$valore))
# Righe uguali a una precedente
duplicated(d)
range(d$valore, na.rm = TRUE)
