# Traslare conserva la dispersione.
a <- 1:5
b <- a + 5
centrati <- a - mean(a)
dilatati <- 2 * centrati + mean(a)
gruppi <- list(A=a, B=b, C=dilatati)
sapply(gruppi, mean) # posizione
sapply(gruppi, sd)   # dispersione
