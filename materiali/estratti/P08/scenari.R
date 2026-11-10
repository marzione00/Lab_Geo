d <- read.csv('dati/cronologia_v3.csv')
z <- read.csv('dati/casuali_comuni_v3.csv')$z
E <- matrix(z[1:3000],500,6,byrow=TRUE)
A <- sweep(E,2,d$sd_scenario_anni,'*')
A <- sweep(A,2,d$eta_cal_BP,'+')
ok <- apply(A,1,function(x) all(diff(x)>0))
stopifnot(sum(ok)==500)
quantile(A[ok,6],c(.025,.5,.975))
