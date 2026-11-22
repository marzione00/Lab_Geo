file <- percorso_risultati("campioni.geojson")
sf::st_write(p,file,driver="GeoJSON",
  layer_options=c("RFC7946=YES","COORDINATE_PRECISION=10"),delete_dsn=TRUE,quiet=TRUE)
q <- sf::st_read(file,quiet=TRUE,stringsAsFactors=FALSE)
data.frame(siti_scritti=nrow(p),siti_riletti=nrow(q),
  ID_uguali=setequal(p$id,q$id),longlat_riletta=sf::st_is_longlat(q),bytes=file.info(file)$size)
stopifnot(nrow(q)==64L,!anyDuplicated(q$id),setequal(p$id,q$id),sf::st_is_longlat(q))
