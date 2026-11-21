bad_crs <- suppressWarnings(
 sf::st_set_crs(geo,32632))
stopifnot(identical(
 sf::st_coordinates(bad_crs),
 sf::st_coordinates(geo)))
