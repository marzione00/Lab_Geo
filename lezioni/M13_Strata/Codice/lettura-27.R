d <- read.csv('dati/cronologia_v3.csv')
u <- read.csv('dati/casuali_comuni_v3.csv')
A <- sweep(matrix(u$z[1:3000],500,6,TRUE),
 2,d$sd_scenario_anni,'*')
A <- sweep(A,2,d$eta_cal_BP,'+')
A <- A[apply(A,1,function(a)all(diff(a)>0)),]
v <- apply(A,1,function(a)
 diff(approx(d$profondita_cm,a,
 xout=c(60,100))$y))
quantile(v,c(.025,.5,.975))
