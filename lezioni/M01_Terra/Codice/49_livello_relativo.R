# Variazioni simulate in mm
tempo <- 0:2
mare <- c(0, 3, 6)
suolo <- c(0, -1, -2)
relativo <- mare - suolo
data.frame(tempo, mare,
           suolo, relativo)
