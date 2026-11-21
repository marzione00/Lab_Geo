d <- read.csv('dati/cronologia_v3.csv')
u <- read.csv('dati/casuali_comuni_v3.csv')
E <- matrix(u$z[1:3000],500,6,byrow=TRUE)
A <- sweep(E,2,d$sd_scenario_anni,'*')
A <- sweep(A,2,d$eta_cal_BP,'+')
ok <- apply(A,1,function(a)all(diff(a)>0))
A_ok <- A[ok,,drop=FALSE]
c(generati=nrow(A),accettati=sum(ok),
 scartati=sum(!ok))
