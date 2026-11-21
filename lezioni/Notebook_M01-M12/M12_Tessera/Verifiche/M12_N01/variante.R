errata <- d;errata[nrow(errata),] <- errata[1,]
esito <- data.frame(righe=nrow(errata),celle_distinte=nrow(unique(errata[c("riga","colonna")])),
  occorrenze_duplicate=sum(duplicated(errata[c("riga","colonna")])|
    duplicated(errata[c("riga","colonna")],fromLast=TRUE)))
esito
stopifnot(esito$righe==720L,esito$celle_distinte==719L)
