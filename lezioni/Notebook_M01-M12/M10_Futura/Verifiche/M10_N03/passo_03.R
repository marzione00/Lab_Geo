z <- diff(diff(train,lag=12),differences=1)
data.frame(livelli=length(train),dopo_differenza_12=length(diff(train,lag=12)),
           doppia_differenza=length(z))
stile_grafico()
plot(z,type="l",col=palette_geo[1],xlab="Anno",ylab="Differenza (ppm)",
     main="Trasformazione diagnostica: (1-B)(1-B^12)")
abline(h=0,lty=2)
