source('R/P10_funzioni.R')
d <- read.csv('dati/campioni_modulo1.csv')
x <- transform(d,volume_cm3=0)
respinto <- tryCatch({
 sintesi_campioni(x); FALSE
},error=function(e) TRUE)
stopifnot(respinto,
 isTRUE(all.equal(sintesi_campioni(d),
 sintesi_campioni(d[nrow(d):1,]))))
