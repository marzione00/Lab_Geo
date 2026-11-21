stopifnot(identical(pred18[13:18],ultimo_anno[1:6]),
          identical(pred18[1:12],ultimo_anno))
data.frame(controllo=c("Primo anno uguale all'ultimo train","Mesi 13-18 ripetono 1-6"),esito=TRUE)
stile_grafico()
plot(1:h18,pred18,type="b",pch=19,col=palette_geo[1],xlab="Mesi dall'origine",
  ylab="CO2 prevista (ppm)",main="Baseline stagionale a 18 mesi")
abline(v=12.5,lty=2)
