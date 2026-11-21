# Esempio simulato: errori correlati.
set.seed(746)
e46 <- as.numeric(arima.sim(
  model = list(ar = 0.75), n = 80))
plot(e46, type = "b",
     xlab = "Ordine temporale",
     ylab = "Errore simulato")
abline(h = 0, lty = 2)
acf(e46, main = "Autocorrelazione")
