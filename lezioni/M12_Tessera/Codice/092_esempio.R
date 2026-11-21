zm <- aggregate(quota_m~unita,d,mean)
zn <- table(d$unita)
stopifnot(sum(zn)==720)
zm
