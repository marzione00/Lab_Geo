pc$rotation[, 1]
# Contributi della prima riga allo score.
a48 <- pc$rotation[, 1]
contributi_riga <- Z[1, ] * a48
sum(contributi_riga)
pc$x[1, 1]
