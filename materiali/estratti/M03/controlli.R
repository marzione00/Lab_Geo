d <- read.csv('dati/fossili_simulati.csv')
x <- d$diametro_tot_um
stopifnot(nrow(d)==160L,all(x>0))
table(d$morfotipo)
c(n=length(x),media=mean(x),sd=sd(x))
quantile(x,c(0,.25,.5,.75,1),type=7)
