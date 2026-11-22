# Media del conteggio: 6
k35 <- 0:qpois(.999, lambda=6)
pr35 <- dpois(k35, lambda=6)
sum(pr35)  # Quasi 1: coda esclusa
c(media=6, varianza=6, sd=sqrt(6))
