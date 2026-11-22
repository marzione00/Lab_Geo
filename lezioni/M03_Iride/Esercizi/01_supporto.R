# Iride M03 - esercizio 01
# Misure individuali e medie di stazione
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m03-supporto
# Aprire Iride_M03.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("setup.R", encoding = "UTF-8")
rA <- lab_supporto(noise = 1, seed = 17)
rB <- lab_supporto(noise = 3, seed = 17)
# Conteggi e medie delle sei stazioni
rbind(A = rA$indicatori, B = rB$indicatori)
rA$medie
rB$medie
