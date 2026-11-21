obs <- as.matrix(p[251:260,c("x_VAR","y_VAR")])
base <- matrix(rep(as.numeric(tail(mod$v,1)),each=h),ncol=2)
confronto <- data.frame(variabile=c("X","Y"),
  RMSE_VAR=sqrt(colMeans((obs-prev)^2)),
  RMSE_ultimo=sqrt(colMeans((obs-base)^2)))
confronto
