r_out <- raster_locale(slope_deg,
 x[2:29],y[2:23])
stopifnot(terra::ncell(r_out)==616,
 all(terra::res(r_out)==30))
