d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 ag <- aggrega_blocchi(Z,2,2);A <- ag$media
 risultato <- data.frame(griglia=c("30 m","60 m"),celle=c(length(Z),length(A)),
   media=c(mean(Z),mean(A)),minimo=c(min(Z),min(A)),massimo=c(max(Z),max(A)))
 risultato
 stopifnot(identical(dim(A),c(12L,15L)),all(ag$numero==4L),
   abs(mean(Z)-mean(A))<1e-10,min(A)>=min(Z),max(A)<=max(Z))
