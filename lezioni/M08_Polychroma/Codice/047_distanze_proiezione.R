DT <- as.matrix(dist(pc$x))
D2 <- as.matrix(dist(pc$x[, 1:2]))
max(D2 - DT)
# Differenza non positiva, salvo
# arrotondamenti numerici.
