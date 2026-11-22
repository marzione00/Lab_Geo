stile_grafico()
plot(1:4,rep(NA_real_,4),type="n",xlim=c(.5,4.5),ylim=c(-.4,.6),xaxt="n",
  xlab="Caso originale",ylab="Indice normalizzato",main="Maschera del denominatore: due casi esclusi")
rect(c(1.7,2.7),-.4,c(2.3,3.3),.6,col="#EDF0F1",border=NA)
axis(1,at=1:4);abline(h=0,col="grey70",lty=3)
points(which(ok),indice[ok],pch=19,cex=1.3,col=palette_geo[1])
text(which(!ok),rep(.1,sum(!ok)),"NA",col=palette_geo[2])
write.csv(risultato,percorso_risultati("maschera_denominatore.csv"),row.names=FALSE,na="")
