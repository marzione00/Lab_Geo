# Aurea M04 - esercizio 05
# Tasso ed esposizione
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m04-poisson
# Aprire Aurea_M04.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("setup.R", encoding = "UTF-8")
# Stesso tasso, esposizione doppia
rA <- lab_poisson(exposure = 3)
rB <- lab_poisson(exposure = 6)
rbind(A = rA$indicatori, B = rB$indicatori)
