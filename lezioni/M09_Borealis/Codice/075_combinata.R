dc75 <- diff(diff(y, lag = 12))
# Cambiare l'ordine produce lo stesso filtro.
alt75 <- diff(diff(y), lag = 12)
stopifnot(isTRUE(all.equal(dc75, alt75)))
plot(dc75, ylab = "Differenza combinata")
acf(dc75, lag.max = 36)
