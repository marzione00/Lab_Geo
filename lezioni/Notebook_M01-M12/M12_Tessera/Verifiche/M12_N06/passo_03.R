stile_grafico()
bp <- barplot(risultato$area_ha,names.arg=risultato$unita,col=palette_geo[1:2],
  ylim=c(0,max(risultato$area_ha)*1.2),xlab="Unita sintetica",ylab="Area planimetrica (ha)",
  main="Dal conteggio delle celle all'area")
text(bp,risultato$area_ha,labels=round(risultato$area_ha,2),pos=3)
write.csv(risultato,percorso_risultati("aree_classi.csv"),row.names=FALSE)
