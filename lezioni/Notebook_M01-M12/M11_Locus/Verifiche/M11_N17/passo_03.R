stile_grafico()
barplot(sintesi$concentrazione,names.arg=sintesi$blocco,col=palette_geo[1:4],
  ylab="Concentrazione media dei siti (u.a.)",main="Quattro blocchi: 16 siti ciascuno")
write.csv(sintesi,percorso_risultati("medie_blocchi.csv"),row.names=FALSE)
