u_xy <- sf::st_coordinates(utm)
d_utm <- as.matrix(dist(u_xy))
c(locale=D[1,2],UTM=d_utm[1,2],
 sfera=haversine(d$lon[1],d$lat[1],
                d$lon[2],d$lat[2]))
