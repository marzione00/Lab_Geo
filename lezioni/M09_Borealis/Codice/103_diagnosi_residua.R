varianti <- list(diff1 = delta1,
                 diff12 = delta12,
                 combinata = deltaC)
sapply(varianti, function(v) {
  a <- as.numeric(acf(as.numeric(v),
    lag.max = 12, plot = FALSE)$acf)
  c(lag1 = a[2], lag12 = a[13])
})
