data.frame(archivio=c("Originale","Con duplicato"),
  n_righe=c(nrow(f),nrow(copia)),n_ID=c(length(unique(f$id)),length(unique(copia$id))),
  media_interno=c(mean(f$diametro_int_um),mean(copia$diametro_int_um)))
