riallineato <- terra::resample(spostato,r,method="bilinear")
v0 <- as.numeric(terra::values(r));v1 <- as.numeric(terra::values(riallineato))
validi <- is.finite(v0)&is.finite(v1)
audit <- data.frame(geometria_target=terra::compareGeom(r,riallineato,stopOnError=FALSE),
  coppie_valide=sum(validi),media_scarto_m=mean(v1[validi]-v0[validi]),
  massimo_scarto_m=max(abs(v1[validi]-v0[validi])))
audit
stopifnot(audit$geometria_target,audit$coppie_valide>0)
