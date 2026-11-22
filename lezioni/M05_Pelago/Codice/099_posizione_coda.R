B99 <- c(40, 200, 1000)
p99 <- .975
h99 <- 1 + (B99-1)*p99
data.frame(B = B99, posizione = h99,
  repliche_coda_circa = B99*(1-p99))
# Il quantile dipende da pochi
# valori vicini alla coda superiore.
