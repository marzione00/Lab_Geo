# Stessi campioni, stessa scala, k=3.
tab90 <- table(Kmeans=km$cluster,
               Ward=ward)
tab90
# I numeri dei gruppi non sono nomi
# geologici ne' ordini di grandezza.
