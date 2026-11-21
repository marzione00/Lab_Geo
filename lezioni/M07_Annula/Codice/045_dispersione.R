# Scala dei residui standardizzati.
rs45 <- rstandard(m0)
plot(fitted(m0), sqrt(abs(rs45)),
     pch = 19, xlab = "Stima (um)",
     ylab = "Radice di |residuo std| ")
lines(lowess(fitted(m0),
             sqrt(abs(rs45))), col = 2)
