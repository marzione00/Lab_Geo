M <- terra::as.matrix(r,wide=TRUE)
attesi <- as.vector(t(M[5:10,10:17]))
risultato <- data.frame(n=length(win),errore=max(abs(win-attesi)),
  bytes_valori_finestra=as.numeric(object.size(win)),bytes_matrice=as.numeric(object.size(M)))
risultato
stopifnot(risultato$errore<1e-10)
