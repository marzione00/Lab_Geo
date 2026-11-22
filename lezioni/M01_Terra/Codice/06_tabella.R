# Tre misure, ciascuna con il suo id
misure <- data.frame(
  id = 1:3,
  stazione = factor(c("A", "A", "B")),
  valore = c(2.9, 3.2, 7.1)
)
str(misure)  # Tipi delle colonne
head(misure) # Prime righe
