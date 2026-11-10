n <- 10; p <- .3
dbinom(3,size=n,prob=p)
pbinom(2,size=n,prob=p,lower.tail=FALSE)
qbinom(.95,size=n,prob=p)
set.seed(404)
k <- rbinom(10000,size=n,prob=p)
c(teoria=n*p,simulazione=mean(k))
stopifnot(all(k>=0 & k<=n))
