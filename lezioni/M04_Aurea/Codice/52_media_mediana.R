set.seed(17)
x52 <- rlnorm(500, 0, .6)
c(mediana_teoria = 1,
  mediana_sim = median(x52),
  media_teoria = exp(.6^2/2),
  media_sim = mean(x52))
