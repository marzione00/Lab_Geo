d <- read.csv('dati/ml_v3.csv')
m <- readRDS('risultati/P11/centroidi_modello.rds')
te <- d$split=='test'
Z <- scale(d[te,m$variabili],
 center=m$centro,scale=m$scala)
D <- sapply(m$classi,function(k)
 rowSums(sweep(Z,2,m$centroidi[k,],'-')^2))
p <- m$classi[max.col(-D,ties.method='first')]
table(osservata=d$litologia[te],prevista=p)
