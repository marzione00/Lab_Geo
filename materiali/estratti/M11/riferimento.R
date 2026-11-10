d <- read.csv('dati/spazio_v3.csv')
p <- sf::st_as_sf(d,coords=c('lon','lat'),
 crs='OGC:CRS84',remove=FALSE)
q <- sf::st_transform(p,32632)
b <- sf::st_coordinates(
 sf::st_transform(q,'OGC:CRS84'))
stopifnot(max(abs(b-as.matrix(
 d[c('lon','lat')]))) < 1e-7)
