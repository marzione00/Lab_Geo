# Un centroide per ciascuna riga.
centri66 <- km$centers[
 km$cluster, , drop = FALSE]
dist266 <- rowSums((Z-centri66)^2)
c(manuale = sum(dist266),
  kmeans = km$tot.withinss)
stopifnot(abs(sum(dist266)-
 km$tot.withinss) < 1e-8)
