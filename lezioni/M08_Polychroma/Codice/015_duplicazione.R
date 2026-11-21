# Ripetere SiO2 cambia la distanza.
Zd <- cbind(Z, SiO2_copia = Z[, "SiO2"])
c(prima = as.matrix(dist(Z))[1, 2],
  dopo = as.matrix(dist(Zd))[1, 2])
