d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
richiedi_terra()
r <- terra::rast(percorso_dati("raster_v3.tif"))
 leggi_finestra <- function(r,row,nrows,col,ncols) {
   terra::readStart(r)
   on.exit(terra::readStop(r))
   terra::readValues(r,row=row,nrows=nrows,col=col,ncols=ncols,mat=FALSE)
 }
 win <- leggi_finestra(r,5,6,10,8)
 data.frame(valori=length(win),minimo=min(win),massimo=max(win),media=mean(win))
 stopifnot(length(win)==48L)
