d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 x <- c(0,30,60,90);classe <- c(1,1,2,2);q <- seq(0,90,15)
 lineare <- approx(x,classe,xout=q)$y
 vicino <- vapply(q,function(v) classe[which.min(abs(x-v))],numeric(1))
 risultato <- data.frame(x=q,lineare_ERRATO=lineare,vicino=vicino)
 risultato
 stopifnot(any(!lineare %in% c(1,2)),all(vicino %in% c(1,2)))
