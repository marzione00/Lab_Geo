D_km <- as.matrix(dist(xy/1000))
stopifnot(max(abs(D_km-D/1000))<1e-12)
stile_grafico()
plot(d$x_m,d$y_m,pch=19,col=palette_geo[1],asp=1,
  xlab="x locale (m)",ylab="y locale (m)",main="Distanza fra due siti estremi")
segments(d$x_m[1],d$y_m[1],d$x_m[64],d$y_m[64],col=palette_geo[2],lwd=2)
write.csv(data.frame(id=d$id,distanza_da_S01_m=D[,1]),
  percorso_risultati("distanze_da_S01.csv"),row.names=FALSE)
