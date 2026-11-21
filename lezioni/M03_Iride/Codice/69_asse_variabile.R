# Scala grafica; dati invariati
plot(l_g,seq_along(l_g),log="x",
     xlab="Grana [mm]",ylab="Indice")
# Nuova variabile: log naturale
hist(l_y,breaks=12,
     xlab="log(grana / 1 mm)",
     main="Grana trasformata")
