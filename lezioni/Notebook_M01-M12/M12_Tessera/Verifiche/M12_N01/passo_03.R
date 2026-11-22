mappa_matrice(Z,titolo="720 celle: centri su una griglia regolare")
write.csv(controlli,percorso_risultati("audit_griglia.csv"),row.names=FALSE)
write.csv(risultato,percorso_risultati("geometria_locale.csv"),row.names=FALSE)
