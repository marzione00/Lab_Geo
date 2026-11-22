# Tellus M02 - esercizio 05
# Chiave duplicata e moltiplicazione delle righe
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m02-join
# Aprire Tellus_M02.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("Tellus_laboratori.R", encoding = "UTF-8")
# Confronta una chiave univoca con una duplicata.
rA <- lab_join("no")
rB <- lab_join("yes")
# siti contiene i metadati; dati contiene il join.
rB$siti
rB$dati
rbind(A = rA$indicatori, B = rB$indicatori)
