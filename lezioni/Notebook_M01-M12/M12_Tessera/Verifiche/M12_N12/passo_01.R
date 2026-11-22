d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 g <- gradienti_centrali(Z)
 h1 <- hillshade_esplicito(g$gx,g$gy,315,45)
 h2 <- hillshade_esplicito(g$gx,g$gy,135,45)
 risultato <- data.frame(azimut=c(315,135),altezza=45,media=c(mean(h1),mean(h2)),
   minimo=c(min(h1),min(h2)),massimo=c(max(h1),max(h2)))
 risultato
 stopifnot(identical(dim(h1),c(22L,28L)),all(h1>=0&h1<=1),all(h2>=0&h2<=1))
