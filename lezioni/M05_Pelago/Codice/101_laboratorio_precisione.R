r101 <- lab_precisione(
  B = 200, seed = 17)
r101$indicatori
plot(r101$dati$x, r101$dati$y,
  xlab = "Ripetizione",
  ylab = "Limite superiore")
mean(r101$campione) # Media fissata
