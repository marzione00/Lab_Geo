# Tellus M02 - esercizio 01
# Parametri e trasformazione dei dati
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m02-progetto
# Aprire Tellus_M02.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("Tellus_laboratori.R", encoding = "UTF-8")
# Due scenari con gli stessi ingressi.
rA <- lab_progetto(a = 1, b = 0)
rB <- lab_progetto(a = 2, b = 1)
# Confronta gli indicatori e le prime tre righe.
rbind(A = rA$indicatori, B = rB$indicatori)
head(rB$dati, 3)
