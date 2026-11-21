r_shift <- terra::shift(r,dx=15)
terra::compareGeom(r,r_shift,
                   stopOnError=FALSE)
r_align <- terra::resample(r_shift,r,
 method="bilinear")
