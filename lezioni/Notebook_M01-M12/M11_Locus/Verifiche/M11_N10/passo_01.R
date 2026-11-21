d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 centro <- c(750,750);raggi <- c(300,600,900)
 dist0 <- sqrt((d$x_m-centro[1])^2+(d$y_m-centro[2])^2)
 selezione <- sapply(raggi,function(r) dist0<=r)
 risultato <- data.frame(raggio_m=raggi,n=colSums(selezione),
   media=vapply(seq_along(raggi),function(j) mean(d$concentrazione[selezione[,j]]),numeric(1)))
 risultato
 stopifnot(all(diff(risultato$n)>=0),all(!selezione[,1]|selezione[,2]),all(!selezione[,2]|selezione[,3]))
