stile_grafico()
qqnorm(res,pch=19,col=palette_geo[1],main="Residui e quantili gaussiani")
qqline(res,col=palette_geo[2],lwd=2)
data.frame(quartile=c("Q1","Mediana","Q3"),valore=as.numeric(quantile(res,c(.25,.5,.75))))
