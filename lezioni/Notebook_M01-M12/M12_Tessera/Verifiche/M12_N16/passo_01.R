d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 breve <- as.vector(Z[,2:30]-Z[,1:29])
 lunga <- as.vector(Z[,11:30]-Z[,1:20])
 risultato <- data.frame(distanza_m=c(30,300),direzione="Est-Ovest",coppie=c(length(breve),length(lunga)),
   media_abs=c(mean(abs(breve)),mean(abs(lunga))),mediana_abs=c(median(abs(breve)),median(abs(lunga))))
 risultato
 stopifnot(length(breve)==696L,length(lunga)==480L)
