source('R/P10_funzioni.R')
d <- read.csv('dati/campioni_modulo1.csv')
s <- sintesi_campioni(d)
stopifnot(nrow(s)==6,
 !('densita'%in%names(d)),
 abs(s$densita[s$stazione=='A1']-2.685)<1e-12)
s
