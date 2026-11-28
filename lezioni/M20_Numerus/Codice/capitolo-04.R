d <- read.csv('dati/frane_v1.csv')
m1 <- glm(frane ~ pendenza + litologia +
  offset(log(area_km2)), poisson, d)
m0 <- update(m1, . ~ . - litologia)
D <- deviance(m0) - deviance(m1)
p <- pchisq(D, 2, lower.tail = FALSE)
round(c(dev_m0 = deviance(m0),
  dev_m1 = deviance(m1), D = D), 2)
signif(p, 3)
