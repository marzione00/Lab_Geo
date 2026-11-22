j <- match(d$id,geo_read$id)
stopifnot(!anyNA(j),
 !anyDuplicated(geo_read$id),
 nrow(geo_read)==nrow(d))
stopifnot(max(abs(
 geo_read$concentrazione[j]-z))<1e-8)
sf::sf_extSoftVersion()
