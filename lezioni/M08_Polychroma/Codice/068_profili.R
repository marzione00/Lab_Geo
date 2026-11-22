# Le medie nelle unita' originali.
prof68 <- aggregate(d[v],
 list(cluster=km$cluster), mean)
prof68
# Oppure si inverte la scala di Z.
mu68 <- sweep(km$centers, 2,
 attr(Z,"scaled:scale"), "*")
mu68 <- sweep(mu68, 2,
 attr(Z,"scaled:center"), "+")
round(mu68[,c("SiO2","densita")],2)
