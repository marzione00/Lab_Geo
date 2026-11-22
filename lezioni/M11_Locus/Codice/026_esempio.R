geo <- sf::st_as_sf(d,
 coords=c("lon","lat"),
 crs="OGC:CRS84",remove=FALSE)
stopifnot(nrow(geo)==64L)
sf::st_crs(geo)$input
