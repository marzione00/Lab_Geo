# Riferimento: tutti i 3 anni fittizi.
mese <- format(demo$data, "%m")
media_mese <- tapply(demo$tmax,
                     mese, mean)
anomalia <- demo$tmax -
  media_mese[mese]
plot(demo$data, anomalia, type = "l",
     xlab="Data", ylab="Scarto [C]")
abline(h = 0, col = "grey50")
