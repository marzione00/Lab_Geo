dettagli <- data.frame(id=d$id,distanza_dal_centro_m=dist0,
  entro300=selezione[,1],entro600=selezione[,2],entro900=selezione[,3])
write.csv(dettagli,percorso_risultati("appartenenza_buffer.csv"),row.names=FALSE)
write.csv(risultato,percorso_risultati("sintesi_buffer.csv"),row.names=FALSE)
risultato
