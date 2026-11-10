d <- read.csv('dati/misure_appaiate_simulate.csv')
stopifnot(!anyDuplicated(d$id))
D <- d$dopo-d$prima
a <- t.test(D)
b <- t.test(d$dopo,d$prima,paired=TRUE)
stopifnot(isTRUE(all.equal(a$p.value,b$p.value)))
c(media=mean(D),a$conf.int)
