d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 D <- as.matrix(dist(d[c("x_m","y_m")]))
 ricerca <- D;diag(ricerca) <- Inf
 j <- apply(ricerca,1,which.min)
 risultato <- data.frame(id=d$id,vicino=d$id[j],distanza_m=ricerca[cbind(seq_len(nrow(d)),j)])
 head(risultato,10)
 stopifnot(all(risultato$id!=risultato$vicino),all(risultato$distanza_m==250),all(diag(D)==0))
