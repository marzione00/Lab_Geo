# Evitare selezioni per posizione.
v <- c("SiO2", "CaO", "MgO", "FeO",
       "densita", "grana_mm",
       "colore", "fossili")
X <- as.matrix(d[v])
stopifnot(all(is.finite(X)),
  all(apply(X, 2, sd) > 0))
dim(X)
