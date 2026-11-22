# Un'alternativa esplicita: k = 4.
set.seed(1601)
km4 <- kmeans(Z,4,nstart=50,
              iter.max=100)
km4$size
table(k3=km$cluster,k4=km4$cluster)
aggregate(d[v],
 list(cluster=km4$cluster),mean)
