d <- read.csv('dati/rocce_simulate.csv')
v <- c('SiO2','CaO','MgO','FeO',
       'densita','grana_mm','colore','fossili')
X <- as.matrix(d[v])
stopifnot(!anyNA(X),all(apply(X,2,sd)>0))
Z <- scale(X)
medie <- attr(Z,'scaled:center')
scale <- attr(Z,'scaled:scale')
head(Z)
