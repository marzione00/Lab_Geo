# Una delle quaranta estrazioni.
set.seed(820)
idx <- sort(sample(1:nrow(Z), 72))
ks <- kmeans(Z[idx, ], 3, nstart = 30,
             iter.max = 100)
outer(ks$cluster, ks$cluster, "==")[1:4, 1:4]
