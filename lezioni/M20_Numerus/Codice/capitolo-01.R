d <- read.csv('dati/frane_v1.csv')
round(c(media = mean(d$frane),
  varianza = var(d$frane),
  zeri = sum(d$frane == 0)), 2)
m <- lm(frane ~ pendenza, data = d)
predict(m, data.frame(pendenza = 4))
