d <- read.csv('dati/composizioni_v1.csv')
x <- as.matrix(d[4:9]); x[x == 0] <- 0.065
b3 <- 0.5*log(x[,1]*x[,2]/(x[,4]*x[,5]))
m <- lm(densita ~ b3 + litologia, data=d)
setNames(round(coef(m), 3),
  c('intercetta','b3','Bas.','Cal.'))
