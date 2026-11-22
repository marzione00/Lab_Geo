d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 P <- outer((0:23)*30,(0:29)*30,function(y,x) 900+.12*x+.08*y)
 gx <- (P[2:23,3:30]-P[2:23,1:28])/60
 gy <- (P[3:24,2:29]-P[1:22,2:29])/60
 risultato <- data.frame(componente=c("gx","gy"),atteso=c(.12,.08),
   media=c(mean(gx),mean(gy)),errore_max=c(max(abs(gx-.12)),max(abs(gy-.08))))
 risultato
 stopifnot(all(risultato$errore_max<1e-12),length(gx)==616L)
