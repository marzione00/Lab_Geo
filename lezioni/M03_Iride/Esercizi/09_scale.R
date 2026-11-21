# Iride M03 - esercizio 09
# Leggere valori positivi su due scale
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m03-scale
# Aprire Iride_M03.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
rA <- lab_scale(sdlog = 0.7, seed = 17)
rB <- lab_scale(sdlog = 1.2, seed = 17)
rbind(A = rA$indicatori, B = rB$indicatori)
# R usa il logaritmo naturale con log()
exp(mean(log(rB$dati$originale)))
