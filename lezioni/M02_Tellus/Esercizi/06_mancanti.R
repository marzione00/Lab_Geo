# Tellus M02 - esercizio 06
# Disponibilità casuale e selezione dei valori elevati
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m02-mancanti
# Aprire Tellus_M02.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("Tellus_laboratori.R", encoding = "UTF-8")
# Usa lo stesso seme per i due meccanismi.
rA <- lab_mancanti("random", rate = 0.3, seed = 17)
rB <- lab_mancanti("high", rate = 0.3, seed = 17)
# !disponibile seleziona le osservazioni escluse.
rbind(A = rA$indicatori, B = rB$indicatori)
range(rB$dati$valore_completo[!rB$dati$disponibile])
