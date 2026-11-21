mappa_matrice(mascherata,titolo="24 celle senza dato: il bianco resta assenza",limiti=range(Z))
write.csv(risultato,percorso_risultati("effetto_NoData.csv"),row.names=FALSE)
write.csv(data.frame(riga=rep(0:23,each=30),colonna=rep(0:29,24),
  disponibile=as.vector(t(!is.na(mascherata)))),percorso_risultati("maschera.csv"),row.names=FALSE)
