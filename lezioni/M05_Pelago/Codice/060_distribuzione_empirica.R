# Quattro osservazioni adimensionali
x60 <- c(4, 5, 7, 8)
F60 <- ecdf(x60)  # Frazione <= t
F60(c(4, 6, 8))  # .25, .50, 1
plot(F60, main = "CDF empirica",
     xlab = "t", ylab = "F_n(t)")
