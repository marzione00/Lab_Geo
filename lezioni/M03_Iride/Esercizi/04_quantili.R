# Iride M03 - esercizio 04
# Allargare una distribuzione intorno al suo centro
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m03-quantili
# Aprire Iride_M03.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
rA <- lab_quantili(noise = 1, n = 60, seed = 17)
rB <- lab_quantili(noise = 2, n = 60, seed = 17)
rbind(A = rA$indicatori, B = rB$indicatori)
# Trasformazione rispetto al centro teorico 10
all.equal(rB$dati$valore, 10 + 2 * (rA$dati$valore - 10))
