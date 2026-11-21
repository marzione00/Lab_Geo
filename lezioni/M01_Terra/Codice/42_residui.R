# Dati didattici con curvatura
x <- 1:8
y <- c(1, 4, 8, 16, 24, 36, 49, 65)
fit <- lm(y ~ x)
plot(fitted(fit), resid(fit),
  xlab = "Stimati", ylab = "Residui")
abline(h = 0, lty = 2)
