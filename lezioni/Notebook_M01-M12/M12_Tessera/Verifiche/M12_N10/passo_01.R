d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
 g <- gradienti_centrali(Z)
 risultato <- data.frame(x_m=rep((1:28)*30,22),y_m=rep((1:22)*30,each=28),
   gradi=as.vector(t(g$gradi)),percento=as.vector(t(g$percento)))
 summary(risultato[c("gradi","percento")])
 stopifnot(nrow(risultato)==616L,all(risultato$gradi>=0&risultato$gradi<90))
