d <- read.csv('dati/cronologia_v3.csv')
q <- c(-10,0,35,100,160,180)
a <- approx(d$profondita_cm,d$eta_cal_BP,
 xout=q,rule=1)$y
stopifnot(abs(a[3]-305) < 1e-12,
 is.na(a[1]),is.na(a[6]))
data.frame(profondita_cm=q,eta_cal_BP=a)
