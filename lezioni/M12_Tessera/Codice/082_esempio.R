I0 <- (NIR-R_band)/(NIR+R_band)
I2 <- (2*NIR-2*R_band)/(2*NIR+2*R_band)
stopifnot(max(abs(I0-I2))<1e-12)
