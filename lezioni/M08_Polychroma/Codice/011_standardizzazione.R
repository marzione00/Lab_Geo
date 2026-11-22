Z <- scale(X, center = TRUE,
           scale = TRUE)
medie <- attr(Z, "scaled:center")
devstd <- attr(Z, "scaled:scale")
# Verificare la trasformazione.
round(colMeans(Z), 10)
apply(Z, 2, sd)
