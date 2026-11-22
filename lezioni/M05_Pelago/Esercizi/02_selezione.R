# Pelago M05 - esercizio 02
# Precisione e bias di selezione
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m05-selezione
# Aprire Pelago_M05.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("setup.R", encoding = "UTF-8")
# Quattro volte piu osservazioni
rA <- lab_selezione(n = 60)
rB <- lab_selezione(n = 240)
rbind(A = rA$indicatori, B = rB$indicatori)
