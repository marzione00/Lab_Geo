d <- read.csv('dati/frane_v1.csv')
m <- glm(frane ~ pendenza + litologia +
  offset(log(area_km2)),
  family = poisson, data = d)
cbind(stima = round(coef(m), 4))
round(exp(10 * coef(m)[['pendenza']]), 3)
