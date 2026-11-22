# Intervalli illustrativi: stima e SE
d25 <- c(0.2, 0.2, 1.0, 1.0)
se25 <- c(0.05, 0.4, 0.2, 0.8)
data.frame(stima = d25,
  minimo = d25 - 1.96 * se25,
  massimo = d25 + 1.96 * se25)
