# La griglia del laboratorio
x <- seq(0, 10, by = 0.5)
lo <- 3; hi <- 8
a <- min(lo, hi); b <- max(lo, hi)
incluso <- x >= a & x <= b
c(inclusi = sum(incluso),
  esclusi = sum(!incluso))
x[incluso]         # Estremi inclusi
