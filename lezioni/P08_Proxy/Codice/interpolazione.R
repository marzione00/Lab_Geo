d <- read.csv('dati/cronologia_v3.csv')
f <- function(z) approx(d$profondita_cm,
 d$eta_cal_BP,xout=z,rule=1)$y
stopifnot(all(diff(d$profondita_cm)>0),
 all(diff(d$eta_cal_BP)>0),
 abs(f(35)-305)<1e-10,
 all(is.na(f(c(-1,161)))))
f(c(35,100,160))
