# Una diversa domanda di somiglianza.
chim71 <- c("SiO2","CaO","MgO","FeO")
Z71 <- scale(d[chim71])
set.seed(819)
km71 <- kmeans(Z71,3,nstart=50)
# Tabella, senza confrontare i nomi.
table(tutte=km$cluster,
      chimica=km71$cluster)
