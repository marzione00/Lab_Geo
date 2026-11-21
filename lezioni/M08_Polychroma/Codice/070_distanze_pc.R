# Tutte le PC: rotazione ortogonale.
D70 <- as.matrix(dist(Z))
T70 <- as.matrix(dist(pc$x))
max(abs(D70-T70))
# Due PC: le distanze si contraggono.
Q70 <- as.matrix(dist(pc$x[,1:2]))
stopifnot(max(Q70-D70)<1e-8)
