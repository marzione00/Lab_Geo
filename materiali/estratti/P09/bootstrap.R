x <- read.csv('dati/estremi_v3.csv')$portata_massima_m3s
q100 <- function(v) {
 b <- sd(v)*sqrt(6)/pi
 a <- mean(v)-0.5772156649015329*b
 a-b*log(-log(.99))
}
I <- as.matrix(read.csv(
 'risultati/P09/bootstrap_indici.csv'))
q <- apply(I,1,function(i) q100(x[i]))
quantile(q,c(.025,.5,.975))
