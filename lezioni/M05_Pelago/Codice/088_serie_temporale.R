r88 <- lab_blocchi(length = 8,
  rho = .7, B = 200, seed = 17)
x88 <- r88$campione
plot(x88, type = "l",
     xlab = "Tempo",
     ylab = "Valore adimensionale")
abline(h = 0, lty = 2)
