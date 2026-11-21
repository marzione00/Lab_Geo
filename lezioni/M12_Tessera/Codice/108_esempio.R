rr <- terra::rast(file_tif)
stopifnot(terra::compareGeom(r_out,rr),
 max(abs(terra::values(rr)-
         terra::values(r_out)))<1e-10)
