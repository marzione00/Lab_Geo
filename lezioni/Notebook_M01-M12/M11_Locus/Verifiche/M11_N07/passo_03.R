limiti <- seq(min(d$concentrazione),max(d$concentrazione),length.out=21)
classe <- cut(d$concentrazione,limiti,include.lowest=TRUE,labels=FALSE)
tab <- data.frame(id=d$id,x_m=d$x_m,y_m=d$y_m,concentrazione=d$concentrazione,
  classe=classe,colore=hcl.colors(20,"Viridis")[classe])
head(tab,6)
write.csv(tab,percorso_risultati("mappa_punti.csv"),row.names=FALSE)
write.csv(data.frame(limite=limiti),percorso_risultati("scala_cromatica.csv"),row.names=FALSE)
