x <- read.csv('dati/estremi_v3.csv')$portata_massima_m3s
gamma <- .5772156649015329
b <- sd(x)*sqrt(6)/pi
a <- mean(x)-gamma*b
stopifnot(b > 0)
c(posizione=a,scala=b)
