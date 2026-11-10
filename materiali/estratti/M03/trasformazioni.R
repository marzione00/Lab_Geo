d <- read.csv('dati/fossili_simulati.csv')
x <- d$diametro_tot_um
z <- as.numeric(scale(x))
stopifnot(abs(mean(z))<1e-12,
          abs(sd(z)-1)<1e-12)
c(media=mean(x),geometrica=exp(mean(log(x))))
range(z)
