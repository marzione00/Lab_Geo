sil <- silhouette_base(km$cluster, dist(Z))
risultati <- data.frame(id = d$id,
  pc$x[, 1:2], kmeans = km$cluster,
  ward = cutree(h, k = 3), silhouette = sil)
write.csv(risultati, "Risultati/campioni.csv",
          row.names = FALSE)
