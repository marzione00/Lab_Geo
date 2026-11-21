shift <- sweep(xy,2,c(200,-300),"+")
stopifnot(isTRUE(all.equal(
 as.matrix(dist(shift)),D)))
stopifnot(isTRUE(all.equal(
 as.matrix(dist(xy/1000)),D/1000)))
