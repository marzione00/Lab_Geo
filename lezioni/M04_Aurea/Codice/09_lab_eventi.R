a09 <- lab_eventi(prob=.3, n=200)
b09 <- lab_eventi(prob=.3, n=800)
a09$indicatori
b09$indicatori
# Cambia la sequenza, lascia fisso p
c09 <- lab_eventi(prob=.3,
  n=800, seed=21)
c09$indicatori
