risultati <- as.data.frame(do.call(rbind,lapply(pred,function(p) metriche(test,p))))
risultati$modello <- rownames(risultati)
rownames(risultati) <- NULL
risultati <- risultati[,c("modello","MAE","RMSE","bias_osservato_meno_previsto")]
risultati
write.csv(risultati,percorso_risultati("metriche_test.csv"),row.names=FALSE)
