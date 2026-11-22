# Due conteggi indipendenti
set.seed(17)
a39 <- rpois(10000, lambda=2)
b39 <- rpois(10000, lambda=4)
s39 <- a39 + b39
c(media=mean(s39), varianza=var(s39))
# La distribuzione esatta e' Pois(6)
