d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 gruppi <- split(d$quota_m,d$unita)
 risultato <- do.call(rbind,lapply(names(gruppi),function(u) data.frame(unita=u,
   media=mean(gruppi[[u]]),sd=sd(gruppi[[u]]),n=length(gruppi[[u]]))))
 rownames(risultato) <- NULL
 risultato
 stopifnot(sum(risultato$n)==720L)
