# Stessa matrice, singoli avvii.
set.seed(818)
W64 <- replicate(20,
 kmeans(Z, centers=3, nstart=1,
        iter.max=100)$tot.withinss)
range(W64)
# Ora molte inizializzazioni.
set.seed(816)
km <- kmeans(Z, 3, nstart=50,
             iter.max=100)
km$tot.withinss
