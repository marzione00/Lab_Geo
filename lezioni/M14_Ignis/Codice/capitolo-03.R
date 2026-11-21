a <- 476.26; b <- 82.96
q <- a-b*log(-log(.99))
c(livello=q,F=exp(-exp(-(q-a)/b)))
