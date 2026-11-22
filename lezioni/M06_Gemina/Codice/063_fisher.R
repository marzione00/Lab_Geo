# Margini: 27 presenze, 33 assenze
a63 <- 0:27
pr63 <- dhyper(a63,27,33,30)
pobs63 <- dhyper(18,27,33,30)
# Bilaterale: includere tabelle
# non piu probabili dell'osservata
sum(pr63[pr63<=pobs63*(1+1e-7)])
T63 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
fisher.test(T63)$p.value
