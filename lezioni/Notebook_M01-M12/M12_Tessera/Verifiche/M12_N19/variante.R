intero <- terra::shift(r,dx=30,dy=0)
data.frame(shift_pixel=(terra::xmin(intero)-terra::xmin(r))/30,
  stessa_geometria=terra::compareGeom(r,intero,stopOnError=FALSE),
  stesso_passo=all(terra::res(r)==terra::res(intero)))
stopifnot(!terra::compareGeom(r,intero,stopOnError=FALSE))
