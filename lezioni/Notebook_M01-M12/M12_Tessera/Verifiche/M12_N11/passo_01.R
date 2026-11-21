d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 a <- c(359,1);radiani <- a*pi/180
 media <- media_circolare(a)
 risultato <- data.frame(arimetica=mean(a),circolare=unname(media["media_gradi"]),
   risultante=unname(media["risultante"]))
 risultato
 stopifnot(abs(risultato$circolare)<1e-8,risultato$risultante>.99)
