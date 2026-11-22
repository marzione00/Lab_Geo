# Stessa granulometria: mm oppure um.
a <- X[, c("SiO2", "grana_mm")]
b <- a
b[, "grana_mm"] <- 1000 * b[, "grana_mm"]
c(mm = as.numeric(dist(a))[1],
  um = as.numeric(dist(b))[1])
