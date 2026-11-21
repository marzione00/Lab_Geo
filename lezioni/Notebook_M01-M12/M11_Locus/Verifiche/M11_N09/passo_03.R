molteplicita <- as.integer(frequenze[d$id])
stile_grafico()
plot(d$x_m,d$y_m,pch=19,col=palette_geo[molteplicita],asp=1,
  xlab="x locale (m)",ylab="y locale (m)",main="Sovrapposizione fra 750 e 1250 m")
abline(v=c(750,1250),lty=2,col="grey50")
write.csv(unione,percorso_risultati("relazioni_sito_zona.csv"),row.names=FALSE)
data.frame(appartenenze=as.integer(names(table(molteplicita))),siti=as.integer(table(molteplicita)))
