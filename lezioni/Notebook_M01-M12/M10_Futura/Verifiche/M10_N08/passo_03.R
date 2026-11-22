stile_grafico()
plot(p$h,p$errore,type="b",pch=19,col=palette_geo[1],xlab="Mesi dall'origine",
     ylab="Osservato - previsto (ppm)",main="Errore per orizzonte")
abline(h=0,lty=2)
write.csv(p,percorso_risultati("errori_intervalli_per_orizzonte.csv"),row.names=FALSE)
