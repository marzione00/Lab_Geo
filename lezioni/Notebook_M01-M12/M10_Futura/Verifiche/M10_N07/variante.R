data.frame(posizione=seq_len(nrow(risultati)),
  ordine_MAE=risultati$modello[order(risultati$MAE)],
  ordine_RMSE=risultati$modello[order(risultati$RMSE)])
