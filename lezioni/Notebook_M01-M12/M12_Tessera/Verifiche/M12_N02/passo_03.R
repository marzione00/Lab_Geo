invertita <- Z[nrow(Z):1,]
confronto <- data.frame(matrice=c("Corretta","Righe invertite"),
  media=c(mean(Z),mean(invertita)),massimo=c(max(Z),max(invertita)),
  quota_SO=c(Z[1,1],invertita[1,1]))
confronto
stopifnot(mean(Z)==mean(invertita),max(abs(Z-invertita))>0)
write.csv(angoli,percorso_risultati("angoli.csv"),row.names=FALSE)
write.csv(confronto,percorso_risultati("controllo_orientamento.csv"),row.names=FALSE)
