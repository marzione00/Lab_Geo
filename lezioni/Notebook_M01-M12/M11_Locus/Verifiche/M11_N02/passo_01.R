d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 invertite <- data.frame(lon=d$lat,lat=d$lon)
 globale <- abs(invertite$lon)<=180 & abs(invertite$lat)<=90
 locale <- invertite$lon>8 & invertite$lon<10 & invertite$lat>44 & invertite$lat<46
 data.frame(controllo=c("Limiti globali","Zona sintetica attesa"),
   passano=c(sum(globale),sum(locale)),totale=nrow(d))
 stopifnot(all(globale),!any(locale))
