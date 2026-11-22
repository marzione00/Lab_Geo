previsioni$distanza_train_m <- apply(dist_te,1,min)
per_colonna <- do.call(rbind,lapply(split(previsioni,previsioni$x_m),function(a)
  data.frame(x_m=a$x_m[1],n=nrow(a),distanza_minima_train_m=mean(a$distanza_train_m),
    MAE=mean(abs(a$errore_IDW)),bias=mean(a$errore_IDW))))
rownames(per_colonna) <- NULL
per_colonna
write.csv(per_colonna,percorso_risultati("errori_per_colonna.csv"),row.names=FALSE)
