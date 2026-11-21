terra::readStart(r)
win <- terra::readValues(r,row=5,
 nrows=6,col=10,ncols=8,mat=FALSE)
terra::readStop(r)
attesi <- as.vector(t(M[5:10,10:17]))
stopifnot(length(win)==48,
 max(abs(win-attesi))<1e-10)
