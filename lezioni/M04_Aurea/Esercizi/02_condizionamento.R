# Aurea M04 - esercizio 02
# Probabilità condizionata
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m04-condizionamento
# Aprire Aurea_M04.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# Cambia soltanto la quota iniziale
rA <- lab_condizionamento(prior = .4)
rB <- lab_condizionamento(prior = .1)
rbind(A = rA$indicatori, B = rB$indicatori)
