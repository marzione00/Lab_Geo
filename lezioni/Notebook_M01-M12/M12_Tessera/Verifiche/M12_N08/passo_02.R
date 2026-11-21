richiedi_terra();r <- terra::rast(percorso_dati("raster_v3.tif"))
codici <- as.numeric(factor(d$unita,levels=sort(unique(d$unita))))
rc <- raster_da_matrice(matrix(codici,24,byrow=TRUE),r)
bersaglio <- terra::shift(terra::rast(r),dx=15,dy=0)
cl_lin <- terra::resample(rc,bersaglio,method="bilinear")
cl_near <- terra::resample(rc,bersaglio,method="near")
quote_lin <- terra::resample(r,bersaglio,method="bilinear")
a <- as.numeric(terra::values(cl_lin));b <- as.numeric(terra::values(cl_near))
prova <- data.frame(metodo=c("Classi bilinear","Classi near","Quote bilinear"),
  celle_valide=c(sum(is.finite(a)),sum(is.finite(b)),sum(is.finite(terra::values(quote_lin)))),
  codici_non_ammessi=c(sum(is.finite(a)&!a %in% c(1,2)),sum(is.finite(b)&!b %in% c(1,2)),NA))
prova
stopifnot(any(is.finite(a)&!a %in% c(1,2)),all(b[is.finite(b)] %in% c(1,2)))
