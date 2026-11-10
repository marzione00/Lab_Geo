d <- read.csv('dati/progetti/rock.csv')
d$A <- 100*d$area_pixels/256^2
c <- aggregate(cbind(A,permeability_md)~core_id,
 d,mean)
c$Y <- log10(c$permeability_md)
f <- lm(Y~A,c)
b <- unname(coef(f)[2])
stopifnot(abs(b-cov(c$A,c$Y)/var(c$A))<1e-12)
confint(f)
summary(f)$coefficients
