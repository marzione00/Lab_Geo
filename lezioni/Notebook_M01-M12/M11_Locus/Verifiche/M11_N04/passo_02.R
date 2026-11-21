altro <- haversine_km(d$lon[1],d$lat[1],d$lon,d$lat)
euclidea_m <- sqrt((d$x_m-d$x_m[1])^2+(d$y_m-d$y_m[1])^2)
stopifnot(max(abs(km-altro))<1e-10)
confronto <- data.frame(id=d$id,locale_m=euclidea_m,sfera_m=1000*km,
  differenza_m=1000*km-euclidea_m)
confronto[c(1,8,57,64),]
