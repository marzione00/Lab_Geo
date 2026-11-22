set.seed(17)  # sequenza riproducibile
x07 <- rbinom(200, 1, prob = .3)
k07 <- seq_along(x07)
f07 <- cumsum(x07) / k07
plot(k07, f07, type = "l",
  ylim = c(0, 1), xlab = "Prove",
  ylab = "Frequenza cumulativa")
abline(h = .3, lty = 2)
