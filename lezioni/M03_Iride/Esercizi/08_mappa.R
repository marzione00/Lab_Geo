# Iride M03 - esercizio 08
# Valori e posizioni sulla mappa
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m03-mappa
# Aprire Iride_M03.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("setup.R", encoding = "UTF-8")
rA <- lab_mappa(gradient = 4, seed = 17)
rB <- lab_mappa(gradient = 0, seed = 17)
rbind(A = rA$indicatori, B = rB$indicatori)
# A seme fisso resta soltanto il termine del gradiente
all.equal(rA$dati$z - rB$dati$z, 4 * rA$dati$x / 20)
