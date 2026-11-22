# Identita' su un vettore numerico.
v74 <- as.numeric(y)
manuale74 <- v74[-1] - head(v74, -1)
stopifnot(isTRUE(all.equal(
  manuale74, as.numeric(diff(y)))))
