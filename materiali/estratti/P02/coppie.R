d <- read.csv('dati/progetti/foraminiferi.csv')
m <- as.integer(format(as.Date(d$date),'%m'))
d$S <- ifelse(m%in%c(10:12,1:3),'S1','S0')
a <- aggregate(diam_mean_um~trap_year+S,d,mean)
w <- reshape(a,idvar='trap_year',
 timevar='S',direction='wide')
w <- w[complete.cases(w),]
delta <- w$diam_mean_um.S1-w$diam_mean_um.S0
stopifnot(length(delta)==4)
mean(delta)
