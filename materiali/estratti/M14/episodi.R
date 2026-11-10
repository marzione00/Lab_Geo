q <- c(2,3,4,12,14,11,5,4,3,2,
 3,12,15,13,5,4,2,1,3,2)
ex <- q > 10
start <- ex & !c(FALSE,head(ex,-1))
gr <- cumsum(start)
picchi <- aggregate(q~gr,
 data.frame(q=q[ex],gr=gr[ex]),max)
stopifnot(sum(ex)==6,sum(start)==2,
 identical(picchi$q,c(14,15)))
picchi
