# Pelago M05 - esercizio 08
# Bootstrap a blocchi circolari
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m05-blocchi
# Aprire Pelago_M05.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("setup.R", encoding = "UTF-8")
# Stessa serie, lunghezza diversa
rA <- lab_blocchi(length = 8)
rB <- lab_blocchi(length = 1)
rbind(A = rA$indicatori, B = rB$indicatori)
