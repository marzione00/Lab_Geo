letto <- terra::rast(file_interno);bordo <- terra::rast(file_bordo)
valori <- matrice_locale(letto);valori_bordo <- matrice_locale(bordo)
centri <- terra::xyFromCell(letto,c(1,terra::ncell(letto)))
audit <- data.frame(controllo=c("Geometria interna","Geometria completa","Risoluzione 30m",
  "616 valori interni","104 NoData bordo","Maschera esatta","Valori interni","Valori completi",
  "Centro NW corretto","Centro SE corretto"),
  esito=c(terra::compareGeom(letto,r_interno,stopOnError=FALSE),
    terra::compareGeom(bordo,r,stopOnError=FALSE),all(terra::res(letto)==30),
    sum(is.finite(valori))==616L,sum(is.na(valori_bordo))==104L,
    identical(is.na(valori_bordo),is.na(completo)),max(abs(valori-s))<1e-10,
    max(abs(valori_bordo-completo),na.rm=TRUE)<1e-10,
    max(abs(centri[1,]-c(500045,4999955)))<1e-9,
    max(abs(centri[2,]-c(500855,4999325)))<1e-9))
audit
stopifnot(all(audit$esito))
crs_letto <- terra::crs(letto,describe=TRUE)[,c("name","authority","code")]
crs_letto
info_interno <- terra::describe(file_interno,print=FALSE)
info_bordo <- terra::describe(file_bordo,print=FALSE)
tag_NoData <- data.frame(file=c(basename(file_interno),basename(file_bordo)),
  sentinel_meno9999=c(any(grepl("NoData Value=-9999",info_interno,fixed=TRUE)),
    any(grepl("NoData Value=-9999",info_bordo,fixed=TRUE))))
tag_NoData
stopifnot(all(as.character(crs_letto$code)=="32632"),all(tag_NoData$sentinel_meno9999))
writeLines(info_interno,percorso_risultati("GDAL_pendenze_interne.txt"))
writeLines(info_bordo,percorso_risultati("GDAL_pendenze_con_bordo.txt"))
write.csv(tag_NoData,percorso_risultati("audit_tag_NoData.csv"),row.names=FALSE)
write.csv(audit,percorso_risultati("audit_consegna.csv"),row.names=FALSE)
writeLines(c("DATI SINTETICI; georeferenziazione UTM fittizia EPSG32632.",
  "CSV: 616 centri locali, righe da Sud a Nord, pendenza in gradi.",
  "GeoTIFF interno: 22x28, passo 30 m, corner NW 500030/4999970.",
  "GeoTIFF completo: 24x30, 104 celle di bordo NoData; NAflag=-9999, FLT8S.",
  "Centri: E=x_locale+500015, N=y_locale+4999295. TIFF da Nord a Sud.",
  paste("terra",packageVersion("terra"))),percorso_risultati("scheda_consegna.txt"))
mappa_matrice(valori,(1:28)*30,(1:22)*30,titolo="Pendenze GeoTIFF rilette: 616 celle",unita="Gradi")
