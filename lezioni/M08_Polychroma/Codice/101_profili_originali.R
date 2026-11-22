profili <- aggregate(d[v],
  list(gruppo = km$cluster), mean)
profili[, c("gruppo", "SiO2",
             "densita", "grana_mm")]
# Esaminare anche dispersione e casi.
