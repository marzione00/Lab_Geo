d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 n <- table(d$unita)
 risultato <- data.frame(unita=names(n),celle=as.numeric(n),
   area_m2=as.numeric(n)*30*30,area_ha=as.numeric(n)*30*30/10000)
 risultato
 stopifnot(sum(risultato$celle)==720L,abs(sum(risultato$area_ha)-64.8)<1e-10)
