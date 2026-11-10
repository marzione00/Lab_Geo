d <- read.csv('dati/fossili_simulati.csv')
x <- d$diametro_tot_um
y <- d$diametro_int_um
c(Pearson=cor(x,y),
  Spearman=cor(x,y,method='spearman'))
fit <- lm(y~x)
stopifnot(abs(coef(fit)[2]-
 cor(x,y)*sd(y)/sd(x))<1e-12)
