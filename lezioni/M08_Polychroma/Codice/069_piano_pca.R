# La PCA serve qui alla figura.
pc <- prcomp(Z, center=FALSE,
             scale.=FALSE)
q69 <- pc$sdev^2 / sum(pc$sdev^2)
plot(pc$x[,1:2], pch=19,asp=1,
     col=km$cluster,
     xlab="PC1", ylab="PC2")
sum(q69[1:2])
