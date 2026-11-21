stile_grafico()
plot(q,lineare,type="b",pch=19,col=palette_geo[2],ylim=c(.8,2.2),
  xlab="Posizione (m)",ylab="Codice numerico della classe",main="Interpolare un codice crea categorie inesistenti")
lines(q,vicino,type="b",pch=17,col=palette_geo[1]);abline(h=c(1,2),col="grey75",lty=3)
legend("topleft",c("Lineare: errato per classi","Vicino: codici validi"),
  col=palette_geo[c(2,1)],pch=c(19,17),lty=1,bty="n",cex=.8)
write.csv(risultato,percorso_risultati("esempio_1D.csv"),row.names=FALSE)
write.csv(prova,percorso_risultati("resample_terra.csv"),row.names=FALSE)
