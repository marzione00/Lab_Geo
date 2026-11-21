# Aurea M04 - esercizio 08
# Precisione Monte Carlo
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m04-monte-carlo
# Aprire Aurea_M04.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# Quattro volte piu repliche
rA <- lab_monte_carlo(B = 200)
rB <- lab_monte_carlo(B = 800)
rbind(A = rA$indicatori, B = rB$indicatori)
