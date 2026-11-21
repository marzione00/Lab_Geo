errato <- sf::st_set_crs(sf::st_set_crs(p,NA),32632)
xy_errate <- sf::st_coordinates(errato)
stopifnot(max(abs(xy_errate-originali))==0)
data.frame(caso=c("ERRATO: etichetta 32632","Corretto: trasformazione"),
  primo_x=c(xy_errate[1,1],xy_corrette[1,1]),
  primo_y=c(xy_errate[1,2],xy_corrette[1,2]),unita_dichiarata="metri")
