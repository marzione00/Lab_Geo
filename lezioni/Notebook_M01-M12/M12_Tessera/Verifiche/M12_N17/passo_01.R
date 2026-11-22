d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 v <- numeric(12);k <- 1L
 for(i in 1:4) for(j in 1:3) {
   v[k] <- mean(Z[((i-1)*6+1):(i*6),((j-1)*10+1):(j*10)])
   k <- k+1L
 }
 data.frame(blocco=1:12,media=v,celle=60)
 stopifnot(abs(mean(v)-mean(Z))<1e-10)
