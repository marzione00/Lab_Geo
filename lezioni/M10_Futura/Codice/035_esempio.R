theta <- 0.6
radice_ma <- polyroot(c(1,theta))
Mod(radice_ma)
stopifnot(Mod(radice_ma)>1)
