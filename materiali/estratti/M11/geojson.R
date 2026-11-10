d <- read.csv('dati/spazio_v3.csv')
p <- sf::st_as_sf(d,coords=c('lon','lat'),
 crs='OGC:CRS84')
f <- tempfile(fileext='.geojson')
sf::st_write(p,f,quiet=TRUE)
q <- sf::st_read(f,quiet=TRUE)
stopifnot(nrow(q)==nrow(p),
 setequal(q$id,p$id),
 isTRUE(all.equal(q$concentrazione,
 p$concentrazione)))
unlink(f)
