stile_grafico()
plot(confronto$locale_m,confronto$sfera_m,pch=19,col=palette_geo[1],
  xlab="Distanza nel piano locale (m)",ylab="Arco sferico (m)",main="Due metriche dichiarate")
abline(0,1,lty=2,col=palette_geo[2])
write.csv(confronto,percorso_risultati("distanze_confrontate.csv"),row.names=FALSE)
data.frame(massimo_scarto_m=max(abs(confronto$differenza_m)))
