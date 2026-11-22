# Due righe della matrice originale.
scarti <- X[1, ] - X[2, ]
sqrt(sum(scarti^2))
# Stesso valore nella matrice distanze.
as.matrix(dist(X))[1, 2]
