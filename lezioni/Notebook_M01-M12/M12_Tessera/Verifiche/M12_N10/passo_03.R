stile_grafico()
hist(risultato$gradi,breaks=20,col=palette_geo[1],border="white",
  xlab="Pendenza (gradi)",ylab="Numero di celle interne",main="Pendenza sintetica: 616 celle interne")
write.csv(risultato,percorso_risultati("pendenze_interne.csv"),row.names=FALSE)
write.csv(conversione,percorso_risultati("conversione_unita.csv"),row.names=FALSE)
