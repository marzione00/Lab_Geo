X2 <- sweep(Z2, 2, pc$scale, "*")
X2 <- sweep(X2, 2, pc$center, "+")
head(cbind(originale = X[, "densita"],
  ricostruita = X2[, "densita"]))
