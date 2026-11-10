d <- read.csv('dati/raster_v3.csv')
d <- d[order(d$riga,d$colonna),]
Z <- matrix(d$quota_m,24,byrow=TRUE)
r <- terra::rast('dati/raster_v3.tif')
M <- as.matrix(r,wide=TRUE)
stopifnot(nrow(r)==24,ncol(r)==30,
 all(terra::res(r)==30),
 max(abs(M-Z[24:1,]))<.001)
