# Pelago M05 - esercizio 06
# Ricampionare il campione osservato
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m05-bootstrap
# Aprire Pelago_M05.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).
# Scrivere una previsione prima di leggere gli indicatori.

source("setup.R", encoding = "UTF-8")
# Piu ricampionamenti dello stesso campione
rA <- lab_bootstrap(B = 200)
rB <- lab_bootstrap(B = 800)
rbind(A = rA$indicatori, B = rB$indicatori)
