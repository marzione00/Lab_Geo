tempo_T <- seq_along(z)
lo20 <- loess(as.numeric(z) ~ tempo_T,
              span = 0.20)
lo60 <- loess(as.numeric(z) ~ tempo_T,
              span = 0.60)
head(cbind(predict(lo20), predict(lo60)))
# Stesse osservazioni, diverso intorno.
