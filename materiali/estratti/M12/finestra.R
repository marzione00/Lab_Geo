r <- terra::rast('dati/raster_v3.tif')
M <- as.matrix(r,wide=TRUE)
terra::readStart(r)
w <- terra::readValues(r,row=5,nrows=6,
 col=10,ncols=8,mat=FALSE)
terra::readStop(r)
z <- as.vector(t(M[5:10,10:17]))
stopifnot(length(w)==48,
 max(abs(w-z)) < 1e-10)
