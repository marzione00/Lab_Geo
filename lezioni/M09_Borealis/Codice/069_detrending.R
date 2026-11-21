# Temperatura sintetica: una retta da verificare.
t69 <- seq_along(z)
fit69 <- lm(as.numeric(z) ~ t69)
res69 <- residuals(fit69)
plot(t69, res69, type = "l",
     xlab = "Mese", ylab = "Residuo")
acf(res69, lag.max = 36)
