dentro80 <- abs(p$errore)<=qnorm(.9)*p$se
data.frame(livello=c(.8,.95),dentro=c(sum(dentro80),sum(p$dentro95)),
  n=nrow(p),quota=c(mean(dentro80),mean(p$dentro95)))
stopifnot(all(!dentro80 | p$dentro95))
