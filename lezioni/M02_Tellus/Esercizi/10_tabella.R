# Tellus M02 - esercizio 10
# Controlli finali su chiavi e unità
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m02-tabella
# Aprire Tellus_M02.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("Tellus_laboratori.R", encoding = "UTF-8")
# Introduci insieme le due anomalie previste.
rA <- lab_tabella(duplicate = "no", unit = "ok")
rB <- lab_tabella(duplicate = "yes", unit = "wrong")
# unique() raccoglie gli identificativi distinti.
rbind(A = rA$indicatori, B = rB$indicatori)
rB$dati
length(unique(rB$dati$id))
