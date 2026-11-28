d <- read.csv('dati/paleomag_v1.csv')
u <- function(D, I) { D <- D * pi/180
  I <- I * pi/180
  cbind(cos(I) * cos(D),
    cos(I) * sin(D), sin(I)) }
s <- colSums(u(d$D, d$I))
m <- s / sqrt(sum(s^2))
Ig <- atan(2 * tan(42 * pi/180))
g <- u(0, Ig * 180 / pi)
psi <- acos(sum(m * g)) * 180 / pi
round(c(I_gad = Ig * 180/pi,
  distanza = psi), 2)
