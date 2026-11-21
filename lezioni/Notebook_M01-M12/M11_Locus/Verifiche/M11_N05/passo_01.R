d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
richiedi_sf()
 p <- sf::st_as_sf(d,coords=c("lon","lat"),crs="OGC:CRS84",remove=FALSE)
 data.frame(oggetti=nrow(p),geometria=as.character(unique(sf::st_geometry_type(p))),
   longlat=sf::st_is_longlat(p),sf_version=as.character(packageVersion("sf")))
 sf::sf_extSoftVersion()
 stopifnot(identical(sf::st_coordinates(p)[,1],d$lon),
   identical(sf::st_coordinates(p)[,2],d$lat))
