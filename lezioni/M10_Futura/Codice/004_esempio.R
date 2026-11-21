T0 <- end(train)
h <- length(test)
c(anno=T0[1], mese=T0[2], h=h)
stopifnot(h == 36L)
