d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 angoli <- data.frame(angolo=c("SO","SE","NO","NE"),riga_csv=c(0,0,23,23),
   colonna_csv=c(0,29,0,29),quota_m=c(Z[1,1],Z[1,30],Z[24,1],Z[24,30]))
 angoli
 stopifnot(Z[1,1]==d$quota_m[d$riga==0&d$colonna==0],
   Z[24,30]==d$quota_m[d$riga==23&d$colonna==29])
