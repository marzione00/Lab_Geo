file_geo <- "Risultati/siti.geojson"
sf::st_write(geo,file_geo,
 driver="GeoJSON",delete_dsn=TRUE,
 layer_options=c("RFC7946=YES",
 "COORDINATE_PRECISION=10"),quiet=TRUE)
geo_read <- sf::st_read(file_geo,
                        quiet=TRUE)
