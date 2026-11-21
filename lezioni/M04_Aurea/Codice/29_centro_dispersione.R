# Parametri del modello
n29 <- 20
p29 <- .3
c(media = n29*p29,
  varianza = n29*p29*(1-p29))
k29 <- 0:n29
sum(k29 * dbinom(k29, n29, p29))
sqrt(n29*p29*(1-p29))  # SD
