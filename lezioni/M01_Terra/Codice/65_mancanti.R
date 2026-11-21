# Esempio con mancante ed estremo.
x <- c(1.2, NA, 1.4, 12)
is.na(x)               # individua NA
sum(!is.na(x))         # disponibili
mean(x)                # risultato: NA
mean(x, na.rm = TRUE)  # usa 3 valori
x[which(x > 10)]       # da verificare
