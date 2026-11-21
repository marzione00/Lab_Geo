flag <- duplicated(copia$id)|duplicated(copia$id,fromLast=TRUE)
segnalazioni <- data.frame(riga=which(flag),copia[flag,],check.names=FALSE)
segnalazioni
write.csv(segnalazioni,percorso_risultati("segnalazioni_duplicati.csv"),row.names=FALSE)
