stile_grafico()
plot(d$x_m,d$y_m,pch=19,col=palette_geo[ifelse(ovest,1,2)],asp=1,
  xlab="x locale (m)",ylab="y locale (m)",main="Ovest x<1000; Est x>=1000")
abline(v=1000,lty=2,col="grey40")
data.frame(id=d$id[d$x_m==1000],x_m=d$x_m[d$x_m==1000],area=aree[d$x_m==1000])
