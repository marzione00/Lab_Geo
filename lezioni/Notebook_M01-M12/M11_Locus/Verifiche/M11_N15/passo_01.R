d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 D <- as.matrix(dist(d[c("x_m","y_m")]))
 G <- .5*outer(d$concentrazione,d$concentrazione,"-")^2
 ind <- which(upper.tri(D),arr.ind=TRUE)
 coppie <- data.frame(i=ind[,1],j=ind[,2],h=D[ind],gamma=G[ind])
 data.frame(siti=nrow(d),coppie=nrow(coppie),attese=choose(nrow(d),2),
   distanza_massima_m=max(coppie$h))
 stopifnot(nrow(coppie)==2016L,all(coppie$i<coppie$j))
