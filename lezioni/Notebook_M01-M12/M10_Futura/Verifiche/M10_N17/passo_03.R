stile_grafico()
matplot(1:h,cbind(obs[,2],prev[,2],base[,2]),type="b",pch=c(19,1,17),lty=c(1,2,3),
  col=palette_geo[1:3],xlab="Passi dall'origine 250",ylab="Y sintetica",
  main="Previsione ricorsiva a origine fissa")
legend("topleft",c("Osservato","VAR","Ultimo valore"),col=palette_geo[1:3],
  pch=c(19,1,17),lty=c(1,2,3),bty="n")
write.csv(data.frame(passo=251:260,X_osservata=obs[,1],Y_osservata=obs[,2],
  X_prevista=prev[,1],Y_prevista=prev[,2]),percorso_risultati("previsioni_VAR.csv"),row.names=FALSE)
