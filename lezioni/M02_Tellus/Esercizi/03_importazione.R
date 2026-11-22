# Tellus M02 - esercizio 03
# Separatore decimale e stato della conversione
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m02-importazione
# Aprire Tellus_M02.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("Tellus_laboratori.R", encoding = "UTF-8")
# Cambia soltanto il simbolo decimale riconosciuto.
rA <- lab_importazione("comma")
rB <- lab_importazione("point")
# Leggi le conversioni prima di confrontare le medie.
rA$dati
rB$dati
rbind(A = rA$indicatori, B = rB$indicatori)
