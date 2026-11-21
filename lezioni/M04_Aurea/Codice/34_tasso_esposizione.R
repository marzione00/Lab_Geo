# Esempio: fratture lungo una linea
rate34 <- 2  # Eventi per metro
L34 <- 3     # Metri osservati
mu34 <- rate34 * L34
mu34         # Conteggio atteso: 6
dpois(0, lambda = mu34)
