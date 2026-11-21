r71 <- lab_bootstrap(
  n = 30, B = 200, seed = 17)
r71$indicatori
# La distribuzione e condizionata
# ai 30 valori del campione.
hist(r71$dati$media,
     xlab = "Media bootstrap",
     main = "Ricampionamento")
