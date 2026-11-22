d <- read.csv('dati/progetti/nile.csv')
stopifnot(nrow(d)==100,
 !anyDuplicated(d$year),
 all(diff(d$year)==1),
 range(d$year)==c(1871,1970))
d$post <- as.integer(d$year>=1898)
table(d$post)
tapply(d$volume_1e8_m3,d$post,mean)
