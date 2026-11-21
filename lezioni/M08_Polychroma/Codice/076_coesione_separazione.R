# Un campione e il proprio gruppo.
D <- dist(Z)
DD76 <- as.matrix(D)
i76 <- 1
g76 <- km$cluster
stessi76 <- which(g76==g76[i76] &
          seq_along(g76)!=i76)
a76 <- mean(DD76[i76,stessi76])
altri76 <- setdiff(unique(g76),
                   g76[i76])
b76 <- min(sapply(altri76,function(g)
 mean(DD76[i76,g76==g])))
c(a=a76,b=b76)
