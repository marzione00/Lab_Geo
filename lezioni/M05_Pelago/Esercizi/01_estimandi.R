# Pelago M05 - esercizio 01
# Media delle misure e media delle stazioni
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m05-estimandi
# Aprire Pelago_M05.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("setup.R", encoding = "UTF-8")
# Cambia il numero di misure in C
rA <- lab_estimandi(nHigh = 40)
rB <- lab_estimandi(nHigh = 10)
rbind(A = rA$indicatori, B = rB$indicatori)
