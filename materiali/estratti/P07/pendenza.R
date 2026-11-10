d <- read.csv('dati/raster_v3.csv')
d <- d[order(d$riga,d$colonna),]
Z <- matrix(d$quota_m,24,byrow=TRUE)
gx <- (Z[2:23,3:30]-Z[2:23,1:28])/60
gy <- (Z[3:24,2:29]-Z[1:22,2:29])/60
g <- sqrt(gx^2+gy^2)
gradi <- atan(g)*180/pi
stopifnot(length(gradi)==616,
 max(abs(100*tan(gradi*pi/180)-100*g))<1e-10)
