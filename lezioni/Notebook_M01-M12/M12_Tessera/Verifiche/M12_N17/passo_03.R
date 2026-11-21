stile_grafico()
hist(b,breaks=20,col=palette_geo[1],border="white",xlab="Media dei blocchi ricampionati (m)",
  ylab="Numero di repliche",main="Bootstrap a blocchi: distribuzione condizionata")
abline(v=mean(v),col=palette_geo[2],lwd=2);abline(v=q,col=palette_geo[3],lty=2,lwd=2)
legend("topright",c("Media della griglia","Quantili 2.5% e 97.5%"),
  col=palette_geo[c(2,3)],lty=c(1,2),bty="n",cex=.75)
write.csv(risultato,percorso_risultati("bootstrap_blocchi.csv"),row.names=FALSE)
write.csv(data.frame(replica=1:300,media=b),percorso_risultati("repliche_blocchi.csv"),row.names=FALSE)
