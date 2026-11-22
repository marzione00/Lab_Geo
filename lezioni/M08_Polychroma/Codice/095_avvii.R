set.seed(818)
W_avvii <- replicate(30, {
  m <- kmeans(Z, 3, nstart = 1,
              iter.max = 100)
  m$tot.withinss
})
range(W_avvii)
