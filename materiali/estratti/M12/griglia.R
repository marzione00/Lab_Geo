d <- read.csv('dati/raster_v3.csv')
d <- d[order(d$riga,d$colonna),]
stopifnot(!anyDuplicated(
 paste(d$riga,d$colonna)),nrow(d)==720)
Z <- matrix(d$quota_m,nrow=24,byrow=TRUE)
stopifnot(Z[1,1]==d$quota_m[1],
 Z[24,30]==tail(d$quota_m,1))
range(Z)
