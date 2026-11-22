# X contiene una colonna di 1 e il predittore.
X <- model.matrix(m0)
head(X)
dim(X)       # 160 righe, 2 colonne.
qr(X)$rank   # Rango della matrice.
