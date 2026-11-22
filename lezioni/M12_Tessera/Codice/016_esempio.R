r <- terra::rast("Dati/raster_v3.tif")
terra::crs(r,describe=TRUE)
stopifnot(terra::ncell(r)==720,
 all(terra::res(r)==30))
