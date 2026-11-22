stile_grafico()
hist(nullo,breaks=15,xlim=range(c(nullo,osservato)),col="#CFE2E5",border="white",
  xlab="Moran I con A binaria",main="100 permutazioni originali: alternativa positiva")
abline(v=osservato,col=palette_geo[2],lwd=2,lty=2)
legend("topright","I osservato",lty=2,lwd=2,col=palette_geo[2],bty="n")
write.csv(data.frame(permutazione=seq_len(B),I=nullo),percorso_risultati("permutazioni_originali.csv"),row.names=FALSE)
write.csv(risultato,percorso_risultati("riferimento_Moran.csv"),row.names=FALSE)
