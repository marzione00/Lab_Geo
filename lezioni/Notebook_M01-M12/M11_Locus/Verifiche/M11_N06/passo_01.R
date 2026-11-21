d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
richiedi_sf()
 p <- sf::st_as_sf(d,coords=c("lon","lat"),crs="OGC:CRS84")
 corretto <- sf::st_transform(p,32632)
 originali <- sf::st_coordinates(p)
 xy_corrette <- sf::st_coordinates(corretto)
 data.frame(caso=c("WGS84 lon-lat","UTM32N trasformato"),
   x=c(originali[1,1],xy_corrette[1,1]),y=c(originali[1,2],xy_corrette[1,2]))
