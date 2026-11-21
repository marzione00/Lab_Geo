d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 rosso <- c(.2,0,1e-10,.3);nir <- c(.4,0,2e-10,.2)
 den <- nir+rosso;soglia <- 1e-6;ok <- den>soglia
 indice <- rep(NA_real_,4);indice[ok] <- (nir[ok]-rosso[ok])/den[ok]
 risultato <- data.frame(caso=1:4,rosso=rosso,NIR=nir,denominatore=den,
   usato=ok,indice=indice)
 risultato
 stopifnot(sum(is.na(indice))==2L)
