med <- rep(median(tr$diametro_int_um),nrow(te))
rbind(Media=metriche(te$diametro_int_um,base),
      Mediana=metriche(te$diametro_int_um,med))
