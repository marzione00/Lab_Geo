d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 controlli <- data.frame(controllo=c("720 celle","Coppie uniche","24 righe","30 colonne",
   "x coerente","y coerente"),esito=c(nrow(d)==720L,!anyDuplicated(d[c("riga","colonna")]),
   setequal(d$riga,0:23),setequal(d$colonna,0:29),all(d$x_m==30*d$colonna),all(d$y_m==30*d$riga)))
 controlli
 stopifnot(all(controlli$esito))
