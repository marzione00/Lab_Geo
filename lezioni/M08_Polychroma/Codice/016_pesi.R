# Esempio: dimezzare il peso di SiO2.
pesi <- rep(1, ncol(Z))
pesi[1] <- 0.5
Zw <- sweep(Z, 2, sqrt(pesi), "*")
as.matrix(dist(Zw))[1:3, 1:3]
