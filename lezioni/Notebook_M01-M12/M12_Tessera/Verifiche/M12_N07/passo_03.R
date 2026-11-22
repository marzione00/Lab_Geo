mappa_matrice(A,xa,ya,titolo="Aggregazione 2 x 2: 180 celle da 60 m",limiti=range(Z))
write.csv(risultato,percorso_risultati("confronto_aggregazione.csv"),row.names=FALSE)
write.csv(data.frame(x_m=rep(xa,12),y_m=rep(ya,each=15),quota_media_m=as.vector(t(A))),
  percorso_risultati("celle_60m.csv"),row.names=FALSE)
