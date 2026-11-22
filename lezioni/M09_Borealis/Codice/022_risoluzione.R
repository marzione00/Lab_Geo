mese_es <- 1:48
segnale_es <- sin(2*pi*mese_es/12) +
              0.35*sin(2*pi*mese_es/3)
blocco3 <- (mese_es - 1) %/% 3
blocco12 <- (mese_es - 1) %/% 12
tapply(segnale_es, blocco3, mean)
tapply(segnale_es, blocco12, mean)
