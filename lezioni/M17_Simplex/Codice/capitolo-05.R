d <- read.csv('dati/composizioni_v1.csv')
b <- d$litologia == 'Basalto'
x <- as.matrix(d[b, 4:9])
g <- exp(colMeans(log(x)))
round(rbind(aritmetico=colMeans(x),
  geometrico=100*g/sum(g)), 2)
