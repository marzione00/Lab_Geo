d <- read.csv('dati/paleomag_v1.csv')
D <- d$D * pi/180; I <- d$I * pi/180
X <- cbind(cos(I) * cos(D),
  cos(I) * sin(D), sin(I))
s <- colSums(X); N <- nrow(X)
R <- sqrt(sum(s^2)); k <- (N-1) / (N-R)
a95 <- acos(1 - (N-R) / R *
  (20^(1/(N-1)) - 1)) * 180 / pi
Dm <- atan2(s[2], s[1]) * 180/pi
round(c(D = Dm %% 360,
  I = asin(s[3] / R) * 180 / pi,
  R = R, k = k, a95 = a95), 2)
