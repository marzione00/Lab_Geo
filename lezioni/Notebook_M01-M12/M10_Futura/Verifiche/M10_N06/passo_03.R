stile_grafico()
plot(c2$dati$data[1:168],as.numeric(train),type="l",col="grey45",
  xlim=range(c2$dati$data),ylim=range(train,previsione$inferiore95,previsione$superiore95),
  xlab="Data",ylab="CO2 (ppm)",main="Previsione a origine fissa")
polygon(c(previsione$data,rev(previsione$data)),
  c(previsione$inferiore95,rev(previsione$superiore95)),
  col=adjustcolor(palette_geo[1],.18),border=NA)
lines(previsione$data,previsione$media,col=palette_geo[1],lwd=2)
abline(v=as.numeric(as.Date("1999-01-01")),lty=2)
