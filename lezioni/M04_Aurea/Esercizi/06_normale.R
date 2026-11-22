# Aurea M04 - esercizio 06
# Standardizzazione e quantili
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m04-normale
# Aprire Aurea_M04.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# Probabilita cumulata uguale
rA <- lab_normale(mu = 10, sd = 2)
rB <- lab_normale(mu = 15, sd = 3)
rbind(A = rA$indicatori, B = rB$indicatori)
