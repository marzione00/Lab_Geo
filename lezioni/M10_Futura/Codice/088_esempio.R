z <- qnorm(0.975)
lo <- fc$previsto-z*fc$se
hi <- fc$previsto+z*fc$se
stopifnot(all(lo<=hi))
