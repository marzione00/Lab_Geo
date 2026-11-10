d <- read.csv('dati/rocce_simulate.csv')
v <- c('SiO2','CaO','MgO','FeO',
       'densita','grana_mm','colore','fossili')
Z <- scale(d[v])
h <- hclust(dist(Z),method='ward.D2')
g <- cutree(h,k=3)
set.seed(808)
k <- kmeans(Z,3,nstart=50)$cluster
table(Kmeans=k,Ward=g)
