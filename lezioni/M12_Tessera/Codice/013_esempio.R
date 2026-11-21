d <- d[order(d$riga,d$colonna),]
stopifnot(nrow(d)==720,
 !anyDuplicated(d[c("riga","colonna")]))
Z <- matrix(d$quota_m,24,30,byrow=TRUE)
stopifnot(Z[1,1]==d$quota_m[1])
