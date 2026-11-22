# Una perturbazione nelle unità di Z.
set.seed(819)
Zp <- Z + matrix(rnorm(length(Z),
  sd = 0.4), nrow(Z))
kp <- kmeans(Zp, 3, nstart = 50,
             iter.max = 100)
accordo_coppie(km$cluster, kp$cluster)
