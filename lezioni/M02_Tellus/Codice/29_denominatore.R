# Contare dati raccolti e usati
x <- c(2, NA, 4)
ok <- is.finite(x)
c(totali = length(x),
  disponibili = sum(ok),
  media = mean(x[ok]))
# Tre righe, due valori: media 3
