# Pelago M05 - esercizio 07
# Ricampionamento per stazioni
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m05-ricampionamento
# Aprire Pelago_M05.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# Cambia la dispersione fra stazioni
rA <- lab_ricampionamento(tau = 2)
rB <- lab_ricampionamento(tau = 0)
rbind(A = rA$indicatori, B = rB$indicatori)
