# Tre valori esclusi dal modello
osservati <- c(10, 12, 15)
previsti <- c(9, 13, 14)
errori <- osservati - previsti
# Unita uguale a quella dei dati
sqrt(mean(errori^2))
