# Aurea M04 - esercizio 09
# Propagare incertezze correlate
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m04-propagazione
# Aprire Aurea_M04.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# rho e cv si riferiscono ai logaritmi
rA <- lab_propagazione(rho = 0)
rB <- lab_propagazione(rho = .8)
rbind(A = rA$indicatori, B = rB$indicatori)
