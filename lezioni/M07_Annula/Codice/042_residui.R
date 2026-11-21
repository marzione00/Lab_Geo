# m0 descrive il diametro interno.
e42 <- residuals(m0)
yhat42 <- fitted(m0)
plot(yhat42, e42, pch = 19,
     xlab = "Valore stimato (um)",
     ylab = "Residuo (um)")
abline(h = 0, lty = 2)
# La curva locale aiuta la lettura.
lines(lowess(yhat42, e42), col = 2)
