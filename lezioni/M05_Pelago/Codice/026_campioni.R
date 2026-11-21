set.seed(17)
# Ogni colonna e' un campione.
c26 <- replicate(4, rexp(6))
round(c26, 2)
m26 <- colMeans(c26)
round(m26, 2)  # Quattro medie
