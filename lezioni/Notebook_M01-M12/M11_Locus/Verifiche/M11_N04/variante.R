km2 <- haversine_km(d$lon[1],d$lat[1],d$lon,d$lat,R=6371.0088)
data.frame(raggio_originale_km=6371,raggio_variante_km=6371.0088,
  variazione_massima_m=max(abs(km2-km))*1000)
stopifnot(max(abs(km2-km*(6371.0088/6371)))<1e-10)
