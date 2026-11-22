set.seed(19056)
# Rumore gaussiano IID.
e56 <- rnorm(300)
acf(e56, lag.max = 24,
    main = "Rumore bianco simulato")
# L'ACF campionaria oscilla attorno a zero.
mean(e56)
var(e56)
