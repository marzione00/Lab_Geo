q <- q[match(d$id,q$id),]
attributi <- sf::st_drop_geometry(q)
coordinate <- sf::st_coordinates(sf::st_transform(q,"OGC:CRS84"))
numeriche <- names(d)[vapply(d,is.numeric,logical(1))]
differenze <- vapply(numeriche,function(n) max(abs(attributi[[n]]-d[[n]])),numeric(1))
audit <- data.frame(colonna=numeriche,massimo_scarto=unname(differenze),tolleranza=1e-8)
audit
audit_geometria <- data.frame(asse=c("longitudine","latitudine"),
  massimo_scarto_gradi=c(max(abs(coordinate[,1]-d$lon)),max(abs(coordinate[,2]-d$lat))),
  tolleranza_gradi=1e-7)
audit_geometria
write.csv(audit_geometria,percorso_risultati("audit_geometria_GeoJSON.csv"),row.names=FALSE)
stopifnot(identical(as.character(q$id),d$id),identical(as.character(q$area),d$area),
  all(differenze<1e-8),max(abs(coordinate[,1]-d$lon))<1e-7,
  max(abs(coordinate[,2]-d$lat))<1e-7,all(sf::st_geometry_type(q)=="POINT"))
write.csv(audit,percorso_risultati("audit_GeoJSON.csv"),row.names=FALSE)
scheda <- c("64 siti SINTETICI; concentrazione in unita arbitrarie.",
  "GeoJSON RFC7946: geometria geografica WGS84, ordine longitudine-latitudine.",
  "Coordinate serializzate con dieci decimali; la precisione non e accuratezza di rilievo.",
  "Attributi x_m/y_m: piano locale metrico senza EPSG; non sono offset UTM.",
  "Attributi lon/lat: georiferimento sintetico approssimato del corso.",
  "Verifica per ID: geometrie POINT, coordinate, numerosita e attributi.",
  paste("sf",packageVersion("sf")),capture.output(sf::sf_extSoftVersion()))
writeLines(scheda,percorso_risultati("scheda_consegna.txt"),useBytes=TRUE)
stile_grafico()
plot(sf::st_geometry(q),axes=TRUE,pch=19,col=palette_geo[1],
  main="GeoJSON riletto: georiferimento sintetico",xlab="Longitudine",ylab="Latitudine")
