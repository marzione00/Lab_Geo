# Iride M03 - esercizio 07
# Una relazione visibile con correlazione piccola
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m03-relazioni
# Aprire Iride_M03.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
rA <- lab_relazioni(shape = "line", noise = 1, seed = 17)
rB <- lab_relazioni(shape = "curve", noise = 1, seed = 17)
rbind(A = rA$indicatori, B = rB$indicatori)
# Ascisse identiche nei due modelli
identical(rA$dati$x, rB$dati$x)
