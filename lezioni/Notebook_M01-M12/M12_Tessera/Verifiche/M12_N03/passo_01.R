d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
richiedi_terra()
r <- terra::rast(percorso_dati("raster_v3.tif"))
 geometria <- data.frame(righe=nrow(r),colonne=ncol(r),celle=terra::ncell(r),
   dx=terra::res(r)[1],dy=terra::res(r)[2],
   xmin=terra::xmin(r),xmax=terra::xmax(r),ymin=terra::ymin(r),ymax=terra::ymax(r))
 geometria
 terra::crs(r,describe=TRUE)[,c("name","authority","code")]
 stopifnot(terra::ncell(r)==720L,all(terra::res(r)==30),
   max(abs(as.vector(terra::ext(r))-c(500000,500900,4999280,5000000)))<1e-9)
