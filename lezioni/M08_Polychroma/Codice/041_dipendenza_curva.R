# Relazione deterministica non lineare.
u <- seq(-2, 2, length.out = 41)
y_curva <- u^2
cor(u, y_curva)
plot(u, y_curva, pch = 19,
  xlab = "x", ylab = "x^2")
