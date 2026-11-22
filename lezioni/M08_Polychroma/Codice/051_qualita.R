peso_PC1 <- pc$rotation[, 1]^2
qualita2 <- rowSums(cor_PC[, 1:2]^2)
data.frame(variabile = v,
  peso_PC1 = peso_PC1,
  rappresentata_2PC = qualita2)
