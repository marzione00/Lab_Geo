d <- read.csv('dati/fossili_simulati.csv')
x <- d$diametro_tot_um
g <- d$morfotipo=='Spiky'
stat <- function(g) mean(x[g])-mean(x[!g])
obs <- stat(g); set.seed(602)
B <- 4000L
tp <- replicate(B,stat(sample(g)))
(1+sum(abs(tp)>=abs(obs)))/(B+1)
