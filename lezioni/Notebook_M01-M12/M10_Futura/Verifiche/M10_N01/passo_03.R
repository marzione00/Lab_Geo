stile_grafico()
plot(c2$dati$data,c2$dati$co2_ppm,type="n",xlab="Data",ylab="CO2 (ppm)",
     main="Train e test: origine dicembre 1998")
lines(c2$dati$data[1:168],c2$dati$co2_ppm[1:168],col=palette_geo[1],lwd=2)
lines(c2$date_test,as.numeric(test),col=palette_geo[2],lwd=2)
abline(v=as.numeric(as.Date("1999-01-01")),lty=2)
legend("topleft",c("Train: 168 mesi","Test: 36 mesi"),col=palette_geo[1:2],lty=1,bty="n")
data.frame(origine="1998-12",bersaglio=as.character(c2$date_test[c(1,12,36)]),h=c(1,12,36))
