rx <- residuals(mod$fit_x); ry <- residuals(mod$fit_y)
cov(cbind(X=rx,Y=ry))
cor(rx,ry)
stile_grafico()
plot(rx,ry,pch=19,col=palette_geo[1],xlab="Residuo X",ylab="Residuo Y",
     main="Scarti contemporanei del sistema")
abline(h=0,v=0,lty=2,col="grey60")
