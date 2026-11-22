# Tellus M02 - esercizio 04
# Numerosità e pesi delle medie
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m02-aggregazioni
# Aprire Tellus_M02.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("Tellus_laboratori.R", encoding = "UTF-8")
# Conserva il seme e modifica la numerosita di A.
rA <- lab_aggregazioni(nA = 50, seed = 17)
rB <- lab_aggregazioni(nA = 10, seed = 17)
# Distingui statistiche campionarie e attese del modello.
rbind(A = rA$indicatori, B = rB$indicatori)
rbind(A = rA$attese, B = rB$attese)
