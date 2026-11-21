d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 dentro <- d$x_m>=300 & d$x_m<=600 & d$y_m>=180 & d$y_m<=510
 risultato <- data.frame(dominio=c("Intero","Finestra"),n=c(nrow(d),sum(dentro)),
   media=c(mean(d$quota_m),mean(d$quota_m[dentro])),
   area_ha=c(nrow(d),sum(dentro))*900/10000)
 risultato
 stopifnot(sum(dentro)==132L)
