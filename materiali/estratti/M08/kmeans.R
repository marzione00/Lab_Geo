d <- read.csv('dati/rocce_simulate.csv')
v <- c('SiO2','CaO','MgO','FeO',
       'densita','grana_mm','colore','fossili')
Z <- scale(d[v])
set.seed(808)
k <- kmeans(Z,centers=3,nstart=50)
k$size
k$tot.withinss
round(k$centers,2)
