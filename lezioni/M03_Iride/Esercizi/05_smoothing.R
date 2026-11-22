# Iride M03 - esercizio 05
# Cambiare il grafico conservando i dati
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m03-smoothing
# Aprire Iride_M03.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("setup.R", encoding = "UTF-8")
rA <- lab_smoothing(bins = 18, bw = 0.5, seed = 17)
rB <- lab_smoothing(bins = 8, bw = 1.5, seed = 17)
# Nessuna osservazione cambia
identical(rA$dati, rB$dati)
rbind(A = rA$indicatori, B = rB$indicatori)
