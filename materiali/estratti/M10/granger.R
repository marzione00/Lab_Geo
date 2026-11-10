p <- read.csv('dati/processi_simulati.csv')
d <- data.frame(y=tail(p$y_VAR,-1),
 yl=head(p$y_VAR,-1),xl=head(p$x_VAR,-1))
r <- lm(y~yl,d)
u <- lm(y~yl+xl,d)
coef(u)
anova(r,u)
stopifnot(nobs(r)==nobs(u))
