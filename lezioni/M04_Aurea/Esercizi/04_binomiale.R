# Aurea M04 - esercizio 04
# Bernoulli e binomiale
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m04-binomiale
# Aprire Aurea_M04.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# n cambia; le repliche restano 400
rA <- lab_binomiale(n = 20)
rB <- lab_binomiale(n = 40)
rbind(A = rA$indicatori, B = rB$indicatori)
