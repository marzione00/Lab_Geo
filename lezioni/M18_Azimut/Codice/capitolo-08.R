d <- read.csv('dati/strati_v1.csv')
t <- (d$immersione + 180) * pi / 180
p <- (90 - d$inclinazione) * pi / 180
X <- cbind(cos(p) * cos(t),
  cos(p) * sin(t), sin(p))
e <- eigen(crossprod(X) / nrow(X))
v <- e$vectors[, 3]
v <- v * sign(v[3])
tr <- atan2(v[2], v[1]) * 180 / pi
round(c(S = e$values,
  trend = tr %% 360,
  plunge = asin(v[3]) * 180 / pi), 3)
