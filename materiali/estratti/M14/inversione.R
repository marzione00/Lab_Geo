x <- read.csv('dati/estremi_v3.csv')$portata_massima_m3s
b <- sd(x)*sqrt(6)/pi
a <- mean(x)-.5772156649015329*b
u <- c(.1,.5,.9,.99)
q <- a-b*log(-log(u))
F <- exp(-exp(-(q-a)/b))
stopifnot(max(abs(F-u)) < 1e-12)
data.frame(u,q,F)
