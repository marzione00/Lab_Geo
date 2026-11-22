h <- haversine(d$lon[1],d$lat[1],
               d$lon[2],d$lat[2])
stopifnot(is.finite(h),h>0)
haversine(0,0,1,0) # arco di 1 grado
