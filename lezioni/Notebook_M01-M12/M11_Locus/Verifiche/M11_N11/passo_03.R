stile_grafico()
plot(d$x_m,d$y_m,type="n",asp=1,xlab="x locale (m)",ylab="y locale (m)",
  main="Un vicino scelto per ordine delle righe")
arrows(d$x_m,d$y_m,d$x_m[j],d$y_m[j],length=.06,col="grey60")
points(d$x_m,d$y_m,pch=19,col=palette_geo[1])
risultato$numero_pareggi <- numero_pareggi
write.csv(risultato,percorso_risultati("vicino_piu_prossimo.csv"),row.names=FALSE)
