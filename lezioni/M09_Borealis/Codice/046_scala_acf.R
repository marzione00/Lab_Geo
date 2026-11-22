a46 <- as.numeric(acf(proc$ar1,
  lag.max = 24, plot = FALSE)$acf)
b46 <- as.numeric(acf(10*proc$ar1 + 5,
  lag.max = 24, plot = FALSE)$acf)
stopifnot(max(abs(a46 - b46)) < 1e-12)
