# Esempio con dipendenza esatta costruita.
x68 <- f$diametro_tot_um
s68 <- f$spessore_um
z68 <- x68 - 2*s68
X68 <- cbind(1, x68, z68, s68)
c(colonne = ncol(X68),
  rango = qr(X68)$rank)
