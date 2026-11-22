chim <- c("SiO2", "CaO", "MgO", "FeO")
set.seed(819)
kc <- kmeans(scale(d[chim]), 3,
              nstart = 50)
accordo_coppie(km$cluster, kc$cluster)
