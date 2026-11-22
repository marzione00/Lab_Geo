d <- read.csv('dati/progetti/rock.csv')
d$A <- 100*d$area_pixels/256^2
c <- aggregate(cbind(A,permeability_md)~core_id,
 d,mean)
c$Y <- log10(c$permeability_md)
f <- lm(Y~A,c)
stopifnot(abs(coef(f)[[2]]-
 cov(c$A,c$Y)/var(c$A))<1e-12)
s <- summary(f)$coefficients
round(cbind(s[,1:2], confint(f)), 4)
