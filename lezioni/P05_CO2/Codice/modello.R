d <- read.csv('risultati/P05/mensile_modelli.csv')
d$m <- factor(d$month,levels=1:12)
f <- lm(co2_ppm~t+m,d)
stopifnot(qr(model.matrix(f))$rank==13)
coef(f)[2]
confint(f)[2,]
