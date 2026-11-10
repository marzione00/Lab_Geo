massa_g <- 107.2
volume_cm3 <- 40
rho <- massa_g/volume_cm3
stopifnot(abs(rho-2.68)<1e-12)
rho
