# Pelago M05 - esercizio 04
# Errore standard con osservazioni correlate
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m05-dipendenza
# Aprire Pelago_M05.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# Stesso n, correlazione differente
rA <- lab_dipendenza(rho = .2)
rB <- lab_dipendenza(rho = 0)
rbind(A = rA$indicatori, B = rB$indicatori)
