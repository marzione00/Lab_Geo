completo <- matrix(NA_real_,24,30);completo[2:23,2:29] <- s
r_completo <- raster_da_matrice(completo,r);names(r_completo) <- "pendenza_gradi"
modello_interno <- terra::crop(terra::rast(r),terra::ext(500030,500870,4999310,4999970))
r_interno <- raster_da_matrice(s,modello_interno);names(r_interno) <- "pendenza_gradi"
file_interno <- percorso_risultati("pendenze_interne.tif")
file_bordo <- percorso_risultati("pendenze_con_bordo_NoData.tif")
terra::writeRaster(r_interno,file_interno,overwrite=TRUE,datatype="FLT8S",NAflag=-9999,gdal="COMPRESS=NONE")
terra::writeRaster(r_completo,file_bordo,overwrite=TRUE,datatype="FLT8S",NAflag=-9999,gdal="COMPRESS=NONE")
data.frame(file=c(basename(file_interno),basename(file_bordo)),
  righe=c(nrow(r_interno),nrow(r_completo)),colonne=c(ncol(r_interno),ncol(r_completo)),
  celle_valide=c(sum(is.finite(s)),sum(is.finite(completo))),
  celle_NoData=c(sum(is.na(s)),sum(is.na(completo))))
