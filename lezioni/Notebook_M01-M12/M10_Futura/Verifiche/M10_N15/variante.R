stato <- c(1,0)
risposta <- matrix(NA_real_,21,2)
risposta[1,] <- stato
for(k in 1:20) { stato <- as.numeric(mod$A%*%stato); risposta[k+1,] <- stato }
head(data.frame(h=0:20,X=risposta[,1],Y=risposta[,2]),6)
stile_grafico()
matplot(0:20,risposta,type="l",lty=1,col=palette_geo[1:2],
  xlab="Passi",ylab="Scostamento dal riferimento",main="Propagazione deterministica con A stimata")
abline(h=0,lty=2)
