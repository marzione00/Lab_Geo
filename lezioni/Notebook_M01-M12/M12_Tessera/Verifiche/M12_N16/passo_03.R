stile_grafico()
bp <- barplot(risultato$media_abs,names.arg=paste(risultato$distanza_m,"m"),col=palette_geo[1:2],
  ylim=c(0,max(risultato$media_abs)*1.22),xlab="Separazione Est-Ovest",ylab="Differenza assoluta media (m)",
  main="Distanza e differenze fra celle")
text(bp,risultato$media_abs,labels=paste0("n=",risultato$coppie),pos=3,cex=.8)
write.csv(risultato,percorso_risultati("differenze_spaziali.csv"),row.names=FALSE)
