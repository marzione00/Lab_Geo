d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 mascherata <- Z;mascherata[5:8,10:15] <- NA_real_
 errata <- mascherata;errata[is.na(errata)] <- 0
 risultato <- data.frame(celle_totali=length(Z),celle_mancanti=sum(is.na(mascherata)),
   copertura=mean(!is.na(mascherata)),media_disponibili=mean(mascherata,na.rm=TRUE),
   media_zero=mean(errata))
 risultato
 stopifnot(sum(is.na(mascherata))==24L)
