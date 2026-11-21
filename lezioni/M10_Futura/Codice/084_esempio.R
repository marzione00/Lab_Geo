metriche(obs, p_hat)
c(MAE=mean(abs(e)),
  RMSE=sqrt(mean(e^2)),
  bias=mean(e))
