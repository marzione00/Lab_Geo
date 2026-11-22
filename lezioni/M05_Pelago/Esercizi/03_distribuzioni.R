# Pelago M05 - esercizio 03
# Distribuzione campionaria della media
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m05-distribuzioni
# Aprire Pelago_M05.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("setup.R", encoding = "UTF-8")
# Due popolazioni con media e varianza 1
rA <- lab_distribuzioni()
rB <- lab_distribuzioni(population = "exp")
rbind(A = rA$indicatori, B = rB$indicatori)
