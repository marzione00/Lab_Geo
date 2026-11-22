# La leva dipende dalla matrice X.
h49 <- hatvalues(m0)
plot(f$diametro_tot_um, h49,
     pch = 19, xlab = "Diametro (um)",
     ylab = "Leva")
c(somma = sum(h49),
  parametri = m0$rank)
