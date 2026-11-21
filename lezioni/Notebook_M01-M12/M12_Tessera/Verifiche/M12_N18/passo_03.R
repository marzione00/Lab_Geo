W <- matrix(win,nrow=6,ncol=8,byrow=TRUE)
mappa_matrice(W[6:1,],seq(270,480,30),seq(420,570,30),
  titolo="Finestra letta dal GeoTIFF: 48 celle",limiti=range(Z))
write.csv(risultato,percorso_risultati("audit_finestra.csv"),row.names=FALSE)
write.csv(data.frame(ordine=seq_along(win),quota_m=win),percorso_risultati("valori_finestra.csv"),row.names=FALSE)
