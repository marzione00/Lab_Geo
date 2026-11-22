# Aurea M04 - esercizio 07
# Variabilità moltiplicativa
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m04-moltiplicazione
# Aprire Aurea_M04.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# Dispersione sulla scala logaritmica
rA <- lab_moltiplicazione(sdlog = .6)
rB <- lab_moltiplicazione(sdlog = 1.2)
rbind(A = rA$indicatori, B = rB$indicatori)
