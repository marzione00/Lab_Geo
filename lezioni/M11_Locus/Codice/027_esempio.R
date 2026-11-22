utm <- sf::st_transform(geo,32632)
head(sf::st_coordinates(utm))
stopifnot(!sf::st_is_longlat(utm))
