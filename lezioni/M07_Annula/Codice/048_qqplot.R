# Quantili dei residui standardizzati.
rs48 <- rstandard(m0)
qqnorm(rs48, pch = 19,
       xlab = "Quantile normale",
       ylab = "Residuo standardizzato")
qqline(rs48, col = 2)
