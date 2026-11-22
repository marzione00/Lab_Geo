vista <- Z;vista[!matrix(dentro,24,byrow=TRUE)] <- NA_real_
mappa_matrice(vista,titolo="Finestra: 132 celle selezionate per centro",limiti=range(Z))
write.csv(risultato,percorso_risultati("confronto_domini.csv"),row.names=FALSE)
write.csv(d[dentro,],percorso_risultati("celle_finestra.csv"),row.names=FALSE)
