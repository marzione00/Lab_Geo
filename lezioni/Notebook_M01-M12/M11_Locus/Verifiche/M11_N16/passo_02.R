stile_grafico()
plot(d$x_m,d$y_m,pch=19,col=ifelse(strada,palette_geo[2],"grey65"),asp=1,ylim=c(0,2150),
  xlab="x locale (m)",ylab="y locale (m)",main="Campionare vicino alla strada")
abline(h=250,lty=2,col="grey50")
legend("topleft",c("Siti selezionati","Altri siti della griglia"),pch=19,
  col=c(palette_geo[2],"grey65"),bty="n")
