# Tellus M02 - esercizio 07
# Plausibilità fisica e segnalazione
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m02-controlli
# Aprire Tellus_M02.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("Tellus_laboratori.R", encoding = "UTF-8")
# Cambia il valore sospetto, mantenendo il seme.
rA <- lab_controlli(bad = 250, seed = 17)
rB <- lab_controlli(bad = 20, seed = 17)
# !nel_dominio individua le righe segnalate.
rbind(A = rA$indicatori, B = rB$indicatori)
rA$dati[!rA$dati$nel_dominio, ]
