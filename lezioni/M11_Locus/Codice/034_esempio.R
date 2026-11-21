ovest <- d$x_m<1000
aggregate(concentrazione~area,
 data=d,FUN=mean)
table(d$area)
stopifnot(sum(ovest)==32L)
