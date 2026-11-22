lag_W <- as.numeric(W%*%v)
retta <- lm(lag_W~v)
pendenza <- unname(coef(retta)["v"])
data.frame(intercetta=coef(retta)[1],pendenza=pendenza,I_W=I_W,I_A=I_A)
stopifnot(abs(pendenza-I_W)<1e-12)
stile_grafico()
plot(v,lag_W,pch=19,col=palette_geo[1],xlab="Scarto dalla media (u.a.)",
  ylab="Media degli scarti vicini con W (u.a.)",main="Diagramma di Moran: pendenza I_W")
abline(h=0,v=0,lty=2,col="grey70");abline(retta,col=palette_geo[2],lwd=2)
