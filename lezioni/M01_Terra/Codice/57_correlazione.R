# Coppie con entrambi i valori.
z <- demo[c("tmin", "tmax")]
ok <- complete.cases(z)
sum(ok)                # n coppie
cor(z$tmin[ok], z$tmax[ok])
plot(z$tmin, z$tmax,
     xlab = "Tmin [C]",
     ylab = "Tmax [C]")
