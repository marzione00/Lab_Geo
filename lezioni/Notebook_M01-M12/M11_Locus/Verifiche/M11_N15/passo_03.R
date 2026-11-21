stile_grafico()
plot(risultato$h,risultato$gamma,type="b",pch=19,col=palette_geo[1],
  ylim=c(0,max(risultato$gamma)*1.15),
  xlab="Distanza media della classe (m)",ylab="Semivarianza media (u.a.^2)",
  main="Semivariogramma empirico per quattro classi")
text(risultato$h,risultato$gamma,labels=paste0("n=",risultato$n),pos=3,cex=.8)
write.csv(risultato,percorso_risultati("semivarianza_classi.csv"),row.names=FALSE)
write.csv(coppie,percorso_risultati("coppie_spaziali.csv"),row.names=FALSE)
