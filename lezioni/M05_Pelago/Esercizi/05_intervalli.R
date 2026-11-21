# Pelago M05 - esercizio 05
# Copertura degli intervalli di confidenza
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m05-intervalli
# Aprire Pelago_M05.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# Formula di Student invariata
rA <- lab_intervalli(rho = 0)
rB <- lab_intervalli(rho = .2)
rbind(A = rA$indicatori, B = rB$indicatori)
