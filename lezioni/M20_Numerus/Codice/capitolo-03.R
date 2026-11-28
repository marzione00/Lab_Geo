d <- read.csv('dati/frane_v1.csv')
lv <- c('Argille', 'Flysch', 'Calcari')
d$litologia <- factor(d$litologia, lv)
m <- glm(frane ~ pendenza + litologia +
  offset(log(area_km2)), poisson, d)
b <- coef(m); s <- sqrt(diag(vcov(m)))
round(exp(cbind(stima = b,
  inf = b - 1.96 * s,
  sup = b + 1.96 * s))[-1, ], 3)
