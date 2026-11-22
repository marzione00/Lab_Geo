# Tellus M02 - esercizio 09
# Precondizione della standardizzazione
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m02-funzioni
# Aprire Tellus_M02.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("Tellus_laboratori.R", encoding = "UTF-8")
# Confronta due ampiezze dello stesso vettore.
rA <- lab_funzioni(spread = 1)
rB <- lab_funzioni(spread = 0)
# Leggi dati e indicatori per ciascuno scenario.
rA$dati
rB$dati
rbind(A = rA$indicatori, B = rB$indicatori)
