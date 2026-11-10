d <- read.csv('dati/spazio_v3.csv')
D <- as.matrix(dist(d[c('x_m','y_m')]))
A <- 1*(D > 0 & D <= 260)
nv <- rowSums(A)
stopifnot(all(nv > 0))
W <- A/nv
stopifnot(max(abs(rowSums(W)-1)) < 1e-12)
head(data.frame(id=d$id,vicini=nv))
