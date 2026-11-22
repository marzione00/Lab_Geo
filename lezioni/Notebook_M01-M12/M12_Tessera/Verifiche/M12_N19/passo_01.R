d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
richiedi_terra()
r <- terra::rast(percorso_dati("raster_v3.tif"))
 spostato <- terra::shift(r,dx=15,dy=0)
 risultato <- data.frame(stessa_forma=nrow(r)==nrow(spostato)&ncol(r)==ncol(spostato),
   stesso_passo=all(terra::res(r)==terra::res(spostato)),
   stessa_geometria=terra::compareGeom(r,spostato,stopOnError=FALSE),
   shift_pixel=(terra::xmin(spostato)-terra::xmin(r))/terra::res(r)[1])
 risultato
 data.frame(raster=c("Originale","Spostato"),xmin=c(terra::xmin(r),terra::xmin(spostato)),
   xmax=c(terra::xmax(r),terra::xmax(spostato)))
 stopifnot(risultato$stessa_forma,risultato$stesso_passo,!risultato$stessa_geometria,
   risultato$shift_pixel==.5)
