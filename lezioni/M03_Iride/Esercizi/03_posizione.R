# Iride M03 - esercizio 03
# La stessa serie con un valore modificato
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m03-posizione
# Aprire Iride_M03.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("setup.R", encoding = "UTF-8")
rA <- lab_posizione(outlier = 15, seed = 17)
rB <- lab_posizione(outlier = 100, seed = 17)
rbind(A = rA$indicatori, B = rB$indicatori)
# Il confronto cambia una sola osservazione
identical(rA$dati$y[1:29], rB$dati$y[1:29])
(100 - 15) / 30
