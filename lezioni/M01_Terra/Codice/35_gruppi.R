# Sei campioni, due proprieta
x <- rbind(c(1, 2), c(2, 1),
  c(2, 2), c(8, 9), c(9, 8), c(9, 9))
z <- scale(x)
set.seed(17)
gruppi <- kmeans(z,
  centers = 2, nstart = 20)
gruppi$cluster
