rt <- sf::st_transform(utm,"OGC:CRS84")
cr0 <- sf::st_coordinates(geo)
cr1 <- sf::st_coordinates(rt)
err <- max(abs(cr1-cr0))
stopifnot(err<1e-7); err
