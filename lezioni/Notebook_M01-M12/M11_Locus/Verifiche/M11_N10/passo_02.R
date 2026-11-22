stile_grafico()
plot(d$x_m,d$y_m,pch=19,col="grey55",asp=1,xlim=c(-200,1800),ylim=c(-200,1800),
  xlab="x locale (m)",ylab="y locale (m)",main="Tre raggi, stesso centro")
angolo <- seq(0,2*pi,length.out=201)
for(j in seq_along(raggi)) lines(centro[1]+raggi[j]*cos(angolo),
  centro[2]+raggi[j]*sin(angolo),col=palette_geo[j],lwd=2)
points(centro[1],centro[2],pch=4,cex=1.5,lwd=2)
