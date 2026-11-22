# Tellus M02 - esercizio 02
# Intersezione di condizioni logiche
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m02-selezioni
# Aprire Tellus_M02.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("Tellus_laboratori.R", encoding = "UTF-8")
# Confronta gli estremi nei due ordini.
rA <- lab_selezioni(lo = 3, hi = 8)
rB <- lab_selezioni(lo = 8, hi = 3)
# identical() richiede uguaglianza esatta.
rA$indicatori
identical(rA$dati$incluso, rB$dati$incluso)
