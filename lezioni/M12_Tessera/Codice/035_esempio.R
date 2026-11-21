r60 <- terra::aggregate(r,fact=2,fun=mean)
m30 <- mean(terra::values(r))
m60 <- mean(terra::values(r60))
stopifnot(terra::ncell(r60)==180,
 abs(m30-m60)<1e-9)
