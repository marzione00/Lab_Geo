d <- read.csv('dati/fratture_v1.csv')
t <- d$direzione[d$famiglia == 'J1']
t <- t * pi / 180
r <- function(a) sqrt(mean(cos(a))^2 +
  mean(sin(a))^2)
m <- atan2(mean(sin(2*t)), mean(cos(2*t)))
round(c(R = r(t), R2 = r(2*t),
  asse = (m / 2 * 180 / pi) %% 180), 3)
