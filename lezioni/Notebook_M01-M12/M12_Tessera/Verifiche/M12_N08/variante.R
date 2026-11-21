identico <- terra::resample(r,r,method="near")
errore <- max(abs(terra::values(identico)-terra::values(r)),na.rm=TRUE)
tolleranza <- 1e-4
data.frame(stessa_geometria=terra::compareGeom(identico,r,stopOnError=FALSE),
  errore_m=errore,tolleranza_m=tolleranza)
stopifnot(errore<tolleranza)
