ritorno <- sf::st_coordinates(sf::st_transform(q,"OGC:CRS84"))
scarti <- data.frame(asse=c("longitudine","latitudine"),
  massimo_scarto_gradi=c(max(abs(ritorno[,1]-d$lon)),max(abs(ritorno[,2]-d$lat))))
scarti
stopifnot(all(scarti$massimo_scarto_gradi<1e-7))
stile_grafico()
par(mar=c(4.6,8,3,1.2))
plot(xy[,1],xy[,2],asp=1,pch=19,col=palette_geo[1],xaxt="n",
  xlab="Est UTM32N (m)",ylab="",main="Georiferimento sintetico trasformato")
axis(1,at=pretty(xy[,1],n=3))
mtext("Nord UTM32N (m)",side=2,line=6,las=0)
write.csv(risultato,percorso_risultati("coordinate_UTM32N.csv"),row.names=FALSE)
write.csv(scarti,percorso_risultati("controllo_ritorno.csv"),row.names=FALSE)
