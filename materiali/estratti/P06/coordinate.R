d <- read.csv('dati/spazio_v3.csv')
xy <- as.matrix(d[c('x_m','y_m')])
stopifnot(nrow(d)==64,!anyDuplicated(d$id),
 all(is.finite(xy)),
 !anyDuplicated(paste(d$x_m,d$y_m)))
D <- as.matrix(dist(xy))
stopifnot(all(diag(D)==0),all(D==t(D)))
