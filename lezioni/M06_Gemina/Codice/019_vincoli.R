# Quattro differenze appaiate
d19 <- c(.4, -.2, .7, .5)
set.seed(17)
# Scambio delle due etichette
# soltanto entro ciascuna coppia.
s19 <- sample(c(-1,1), 4,
              replace=TRUE)
mean(s19*d19)
