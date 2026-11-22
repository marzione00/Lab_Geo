# Ricostruzione della sola PC1.
R1 <- pc$x[, 1] %o% pc$rotation[, 1]
R1_opposta <- (-pc$x[, 1]) %o%
              (-pc$rotation[, 1])
max(abs(R1 - R1_opposta))
