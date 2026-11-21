stile_grafico()
matplot(1:h,cbind(ultimo,stagionale,pred_deriva),type="l",lty=c(2,1,1),
  col=palette_geo[1:3],lwd=2,xlab="Mesi dall'origine",ylab="CO2 prevista (ppm)",
  main="Riferimenti disponibili nel dicembre 1998")
legend("topleft",c("Ultimo valore","Stagionale","Deriva"),col=palette_geo[1:3],lty=c(2,1,1),bty="n")
