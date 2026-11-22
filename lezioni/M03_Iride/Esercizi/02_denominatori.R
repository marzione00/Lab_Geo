# Iride M03 - esercizio 02
# Contare gli eventi e dichiarare il denominatore
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m03-denominatori
# Aprire Iride_M03.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
rA <- lab_denominatori(nB = 100, scale = "count")
rB <- lab_denominatori(nB = 200, scale = "rate")
# valore segue la rappresentazione scelta
rA$dati
rB$dati
rbind(A = rA$indicatori, B = rB$indicatori)
