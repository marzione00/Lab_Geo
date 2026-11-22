# Aurea M04 - esercizio 01
# Eventi e frequenze
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m04-eventi
# Aprire Aurea_M04.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# Probabilita fissa, sequenza piu lunga
rA <- lab_eventi(n = 200)
rB <- lab_eventi(n = 800)
rbind(A = rA$indicatori, B = rB$indicatori)
