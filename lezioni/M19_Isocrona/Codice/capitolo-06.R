source('R/york.R')
d <- read.csv('dati/isocrone_v1.csv')
f <- d[d$suite == 'filone', ]
y <- with(f, york(Rb87Sr86, sRb,
  Sr87Sr86, sSr))
lam <- 1.3972e-11; b <- y[['b']]
st <- y[['sb']] / (lam * (1 + b)) / 1e6
round(c(eta = log(1 + b) / lam / 1e6,
  s = st,
  s_scalato = st * sqrt(y[['mswd']])), 2)
