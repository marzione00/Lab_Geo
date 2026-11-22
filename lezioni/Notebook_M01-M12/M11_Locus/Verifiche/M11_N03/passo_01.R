d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 xy <- as.matrix(d[c("x_m","y_m")])
 D <- as.matrix(dist(xy))
 stopifnot(max(abs(D-t(D)))<1e-12,all(diag(D)==0),D[1,2]==250)
 data.frame(siti=nrow(D),celle=length(D),coppie_non_ordinate=choose(nrow(D),2),
   distanza_S01_S64_m=D[1,64])
 head(data.frame(id=d$id,distanza_da_S01_m=D[,1]),10)
