d <- read.csv('dati/campioni_modulo1.csv')
u <- read.csv('dati/casuali_comuni_v3.csv')$u
ix <- matrix(floor(24*u[1:240])+1,
 nrow=10,byrow=TRUE)
rho <- d$massa_g/d$volume_cm3
b <- apply(ix,1,function(i)mean(rho[i]))
stopifnot(all(ix>=1 & ix<=24))
data.frame(replica=1:10,media=b)
