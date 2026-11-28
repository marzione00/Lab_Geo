lam <- 1.3972e-11
sl <- 0.0045e-11 / 2
t <- 301.10; st <- 1.180
sc <- t * sl / lam
round(c(analitica = st, costante = sc,
  totale = sqrt(st^2 + sc^2)), 3)
