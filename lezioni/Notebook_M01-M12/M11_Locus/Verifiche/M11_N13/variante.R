z2 <- 10*d$concentrazione+7
I2 <- moran_I(z2,A)
data.frame(I_originale=I_A,I_trasformato=I2,scarto=I2-I_A)
stopifnot(abs(I2-I_A)<1e-12)
