write.csv(dettaglio,percorso_risultati("previsioni_CV.csv"),row.names=FALSE)
write.csv(cv,percorso_risultati("metriche_CV.csv"),row.names=FALSE)
stile_grafico()
matplot(cv$origine,cv[,c("RMSE_SARIMA","RMSE_Stagionale")],type="b",pch=c(19,17),
  lty=1,col=palette_geo[1:2],xlab="Indice origine",ylab="RMSE a 12 mesi (ppm)",
  main="Validazione interna al train")
legend("topleft",c("SARIMA","Stagionale"),col=palette_geo[1:2],pch=c(19,17),lty=1,bty="n")
