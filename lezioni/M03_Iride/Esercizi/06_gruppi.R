# Iride M03 - esercizio 06
# Separare differenza delle medie e dispersione
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m03-gruppi
# Aprire Iride_M03.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
rA <- lab_gruppi(delta = 1, ratio = 1, seed = 17)
rB <- lab_gruppi(delta = 1, ratio = 2, seed = 17)
rbind(A = rA$indicatori, B = rB$indicatori)
# Il gruppo A non viene modificato
identical(rA$dati$valore[1:70], rB$dati$valore[1:70])
