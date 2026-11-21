ordine <- order(r)
stile_grafico()
matplot(r[ordine],pesi[ordine,],type="l",lty=1,col=palette_geo[1:3],lwd=2,
  xlab="Distanza dal punto richiesto (m)",ylab="Peso normalizzato",main="IDW: sensibilita alla potenza")
legend("topright",paste("p=",potenze),col=palette_geo[1:3],lty=1,lwd=2,bty="n")
write.csv(risultato,percorso_risultati("IDW_potenze.csv"),row.names=FALSE)
write.csv(data.frame(id=d$id,distanza_m=r,p1=pesi[,1],p2=pesi[,2],p3=pesi[,3]),
  percorso_risultati("IDW_pesi.csv"),row.names=FALSE)
stopifnot(abs(idw_pred(xy,d$concentrazione,matrix(posizione,nrow=1),2)-q[2])<1e-12)
