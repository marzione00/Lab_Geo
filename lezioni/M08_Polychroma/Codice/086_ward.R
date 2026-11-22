# Distanze euclidee ordinarie.
D <- dist(Z, method="euclidean")
h <- hclust(D, method="ward.D2")
plot(h,labels=FALSE,
     xlab="Campioni",sub="Ward.D2",
     ylab="Altezza")
tail(h$height,3)
