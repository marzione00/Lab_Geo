S <- crossprod(Z) / (nrow(Z) - 1)
max(abs(S - cov(Z)))
# Su colonne standardizzate, S è
# anche la matrice di correlazione.
max(abs(S - cor(X)))
