x <- read.csv('dati/estremi_v3.csv')$portata_massima_m3s
b <- sd(x)*sqrt(6)/pi
a <- mean(x)-0.5772156649015329*b
Q <- function(p) a-b*log(-log(p))
F <- function(q) exp(-exp(-(q-a)/b))
q100 <- Q(.99)
stopifnot(b>0,abs(F(q100)-.99)<1e-12)
c(a=a,b=b,q100=q100,q500=Q(.998))
