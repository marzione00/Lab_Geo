D <- as.matrix(dist(xy))
stopifnot(all(diag(D)==0),
 isTRUE(all.equal(D,t(D))),
 all(D>=0))
