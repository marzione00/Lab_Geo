# Aurea M04 - esercizio 03
# Densità e probabilità cumulata
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m04-distribuzione
# Aprire Aurea_M04.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# Le aree usano la normale completa
rA <- lab_distribuzione(cut = 1)
rB <- lab_distribuzione(cut = 0)
rbind(A = rA$indicatori, B = rB$indicatori)
