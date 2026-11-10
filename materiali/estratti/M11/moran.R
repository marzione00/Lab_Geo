d <- read.csv('dati/spazio_v3.csv')
D <- as.matrix(dist(d[c('x_m','y_m')]))
A <- 1*(D > 0 & D <= 260)
v <- d$concentrazione-mean(d$concentrazione)
I <- length(v)/sum(A)*
 sum(A*outer(v,v))/sum(v^2)
I_m <- length(v)/sum(A)*
 as.numeric(t(v)%*%A%*%v)/sum(v^2)
stopifnot(abs(I-I_m) < 1e-12)
I
