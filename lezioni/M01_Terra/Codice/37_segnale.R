set.seed(17)
t <- 1:30
segnale <- 2 + 0.1 * t
# Scarti indipendenti simulati
x <- segnale + rnorm(30, sd = 0.6)
plot(t, x, xlab = "Tempo",
     ylab = "Valore simulato")
lines(t, segnale, col = "purple")
