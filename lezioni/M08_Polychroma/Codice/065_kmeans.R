# Otto colonne standardizzate in Z.
set.seed(816)
km <- kmeans(Z, centers = 3,
             nstart = 50,
             iter.max = 100)
km$size
round(km$centers, 2)
c(WSS = km$tot.withinss,
  totale = km$totss)
