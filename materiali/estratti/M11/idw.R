d <- read.csv('dati/spazio_v3.csv')
r <- sqrt((d$x_m-900)^2+(d$y_m-900)^2)
stopifnot(all(r > 0))
w <- r^-2; w <- w/sum(w)
q <- sum(w*d$concentrazione)
stopifnot(abs(sum(w)-1) < 1e-12,
 q >= min(d$concentrazione),
 q <= max(d$concentrazione))
q
