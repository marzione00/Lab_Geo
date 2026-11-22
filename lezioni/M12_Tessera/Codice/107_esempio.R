file_tif <- file.path("Risultati",
 "pendenze_slide.tif")
terra::writeRaster(r_out,file_tif,
 overwrite=TRUE,datatype="FLT8S",
 NAflag=-9999,gdal="COMPRESS=NONE")
