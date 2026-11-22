d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 lon <- d$lon*pi/180;lat <- d$lat*pi/180
 h <- sin((lat-lat[1])/2)^2+cos(lat)*cos(lat[1])*sin((lon-lon[1])/2)^2
 km <- 2*6371*asin(sqrt(pmin(1,pmax(0,h))))
 stopifnot(km[1]==0,all(km>=0))
 head(data.frame(id=d$id,distanza_sferica_km=km),10)
