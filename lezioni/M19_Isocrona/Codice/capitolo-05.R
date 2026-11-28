source('R/york.R')
d <- read.csv('dati/isocrone_v1.csv')
f <- d[d$suite == 'filone', ]
y <- with(f, york(Rb87Sr86, sRb,
  Sr87Sr86, sSr))
df <- nrow(f) - 2
round(c(mswd = y[['mswd']],
  soglia = 1 + 2 * sqrt(2 / df),
  p = pchisq(y[['mswd']] * df, df,
    lower.tail = FALSE)), 4)
