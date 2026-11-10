d <- read.csv('dati/fossili_simulati.csv')
x <- d$diametro_tot_um[d$morfotipo=='Spiky']
y <- d$diametro_tot_um[d$morfotipo=='Rounded']
wilcox.test(x,y,exact=FALSE,correct=TRUE)
U <- sum(outer(x,y,'>'))+
 .5*sum(outer(x,y,'=='))
U/(length(x)*length(y))
