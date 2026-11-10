d <- read.csv('dati/campioni_modulo1.csv')
d$rho <- d$massa_g/d$volume_cm3
s <- aggregate(rho~affioramento,d,mean)
f <- tempfile(fileext='.csv')
write.csv(s,f,row.names=FALSE)
q <- read.csv(f)
stopifnot(identical(q$affioramento,s$affioramento),
 max(abs(q$rho-s$rho))<1e-12)
unlink(f)
s
