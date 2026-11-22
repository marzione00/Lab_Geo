set.seed(19095)
x95 <- c(rep(0, 80), rep(2, 80)) + rnorm(160)
plot(x95, type = "l", ylab = "Valore")
abline(v = 80.5, col = "darkorange")
# Consultare i metadati prima dei test.
c(media_prima = mean(x95[1:80]),
  media_dopo = mean(x95[81:160]))
