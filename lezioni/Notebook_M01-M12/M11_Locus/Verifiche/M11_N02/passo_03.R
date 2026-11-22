stile_grafico()
plot(c(d$lon,invertite$lon),c(d$lat,invertite$lat),type="n",asp=1,
  xlab="Longitudine dichiarata (gradi)",ylab="Latitudine dichiarata (gradi)",
  main="Coordinate corrette e assi scambiati")
points(d$lon,d$lat,pch=19,col=palette_geo[1])
points(invertite$lon,invertite$lat,pch=17,col=palette_geo[2])
legend("center",c("Ordine lon, lat","Ordine invertito"),pch=c(19,17),col=palette_geo[1:2],bty="n")
write.csv(data.frame(id=d$id,globale=globale,locale=locale),
  percorso_risultati("controllo_inversione.csv"),row.names=FALSE)
