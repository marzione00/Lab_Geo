source('R/york.R')
d <- read.csv('dati/isocrone_v1.csv')
g <- d[d$suite == 'granito', ]
f <- with(g, york(Rb87Sr86, sRb,
  Sr87Sr86, sSr))
lam <- 1.3972e-11; b <- f[['b']]
t <- log(1 + b) / lam / 1e6
st <- f[['sb']] / (lam * (1 + b)) / 1e6
round(f[c('a', 'sa', 'b', 'sb')], 7)
round(c(mswd = f[['mswd']], eta = t,
  s_eta = st), 3)
