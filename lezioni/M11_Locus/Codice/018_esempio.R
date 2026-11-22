ok_limiti <- function(lon,lat) {
 all(abs(lon)<=180 & abs(lat)<=90)
}
c(corretti=ok_limiti(d$lon,d$lat),
 invertiti=ok_limiti(d$lat,d$lon))
