d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
richiedi_sf()
 p <- sf::st_as_sf(d,coords=c("lon","lat"),crs="OGC:CRS84",remove=FALSE)
 stopifnot(sf::st_is_longlat(p),!anyDuplicated(p$id))
 data.frame(siti=nrow(p),geometria=as.character(unique(sf::st_geometry_type(p))),
   CRS_ingresso=sf::st_crs(p)$input,attributi=ncol(sf::st_drop_geometry(p)))
