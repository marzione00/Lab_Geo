errori <- sapply(pred,function(p) as.numeric(test)-p)
stile_grafico()
matplot(1:h,errori,type="l",lty=1,col=palette_geo,lwd=1.7,
  xlab="Mesi dall'origine",ylab="Osservato - previsto (ppm)",main="Errori nel test storico")
abline(h=0,lty=2)
legend("topleft",names(pred),col=palette_geo,lty=1,bty="n",cex=.8)
