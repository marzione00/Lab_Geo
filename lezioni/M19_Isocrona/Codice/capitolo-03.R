d <- read.csv('dati/isocrone_v1.csv')
g <- d[d$suite == 'granito', ]
m <- lm(Sr87Sr86 ~ Rb87Sr86, data = g)
b <- coef(m)[[2]]
round(c(iniziale = coef(m)[[1]],
  pendenza = b,
  eta_Ma = log(1 + b) / 1.3972e-11 / 1e6),
  5)
