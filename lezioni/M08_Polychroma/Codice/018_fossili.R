f <- read.csv("Dati/fossili_simulati.csv")
M <- as.matrix(f[c("diametro_tot_um",
  "diametro_int_um", "spessore_um")])
max(abs(M[, 1] - M[, 2] - 2*M[, 3]))
prcomp(M, scale. = TRUE)$sdev
