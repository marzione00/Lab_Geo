d <- read.csv('dati/correnti_v1.csv')
a <- d$azimut * pi / 180
m <- atan2(mean(sin(a)), mean(cos(a)))
round(c(aritmetica = mean(d$azimut),
  circolare = (m * 180 / pi) %% 360), 1)
