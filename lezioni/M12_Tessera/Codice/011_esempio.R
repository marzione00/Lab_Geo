M <- as.matrix(r,wide=TRUE)
Z_nord <- Z[nrow(Z):1,]
max(abs(M-Z_nord))
