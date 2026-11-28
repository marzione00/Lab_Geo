d <- read.csv('dati/isocrone_v1.csv')
g <- d[d$suite == 'granito', ]
lambda <- 1.3972e-11
r0 <- 0.704
t <- log(1 + (g$Sr87Sr86 - r0) /
  g$Rb87Sr86) / lambda / 1e6
i <- c(1, 5, 10)
round(setNames(t, g$campione)[i])
