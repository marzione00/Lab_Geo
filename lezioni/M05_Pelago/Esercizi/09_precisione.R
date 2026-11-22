# Pelago M05 - esercizio 09
# Stabilità numerica di un quantile
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m05-precisione
# Aprire Pelago_M05.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# Trenta ripetizioni per ciascun B
rA <- lab_precisione(B = 200)
rB <- lab_precisione(B = 800)
rbind(A = rA$indicatori, B = rB$indicatori)
