celle <- c(1,30,691,720)
centri <- terra::xyFromCell(r,celle)
risultato <- data.frame(cella_TIFF=celle,E=centri[,1],N=centri[,2],
  x_locale=centri[,1]-500015,y_locale=centri[,2]-4999295)
risultato
stopifnot(identical(as.numeric(centri[1,]),c(500015,4999985)))
