# Curva teorica: eta varia da -4 a 4.
eta73 <- seq(-4, 4, length.out = 101)
plot(eta73, plogis(eta73), type = "l",
     xlab = "Predittore lineare eta",
     ylab = "Probabilita'", ylim = c(0, 1))
abline(h = 0.5, v = 0, lty = 2)
