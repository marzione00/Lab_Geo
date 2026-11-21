stile_grafico()
boxplot(quota_m~unita,data=d,col=palette_geo[1:2],xlab="Unita sintetica",ylab="Quota (m)",
  main="Distribuzione delle quote per zona")
points(seq_len(nrow(risultato)),risultato$media,pch=18,cex=1.3,col="#15283E")
legend("topleft","Rombo: media zonale",pch=18,col="#15283E",bty="n",cex=.8)
write.csv(risultato,percorso_risultati("statistiche_zonali.csv"),row.names=FALSE)
write.csv(controllo,percorso_risultati("controllo_pesi_zonali.csv"),row.names=FALSE)
