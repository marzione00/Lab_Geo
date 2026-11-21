r100a <- lab_precisione(
  B = 200, seed = 17)
r100b <- lab_precisione(
  B = 1000, seed = 17)
c(B200 = sd(r100a$dati$y),
  B1000 = sd(r100b$dati$y))
identical(r100a$campione,
          r100b$campione)
