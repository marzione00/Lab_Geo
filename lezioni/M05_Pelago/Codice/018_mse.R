# Modello della slide precedente
n18 <- 60
bias18 <- -1
var18 <- 4/n18
mse18 <- var18+bias18^2
c(varianza=var18,bias=bias18,
  mse=mse18,rmse=sqrt(mse18))
