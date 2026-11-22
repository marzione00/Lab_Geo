errori <- data.frame(id=te$id,morfotipo=te$morfotipo,errore=te$diametro_int_um-prev)
aggregate(errore~morfotipo,data=errori,FUN=mean)
aggregate(abs(errore)~morfotipo,data=errori,FUN=mean)
write.csv(errori,percorso_risultati("errori_per_individuo.csv"),row.names=FALSE)
