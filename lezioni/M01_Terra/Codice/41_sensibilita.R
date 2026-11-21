x <- c(3, 4, 5, 6, 7, 8, 16)
confronto <- c(
  media = mean(x),
  mediana = median(x),
  senza_massimo = mean(x[x < 16]))
# Ultima riga: scenario di sensibilita
confronto
