# WSS della partizione di Ward.
mu92 <- rowsum(Z,ward) /
         as.vector(table(ward))
W92 <- sum((Z-mu92[ward,])^2)
c(Kmeans=km$tot.withinss,Ward=W92)
# Nello stesso spazio, confrontiamo
# la stessa quantita' geometrica.
