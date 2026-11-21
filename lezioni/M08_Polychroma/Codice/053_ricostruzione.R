Z2 <- pc$x[, 1:2, drop = FALSE] %*%
  t(pc$rotation[, 1:2, drop = FALSE])
sqrt(mean((Z - Z2)^2))
# RMSE nelle unità standardizzate.
