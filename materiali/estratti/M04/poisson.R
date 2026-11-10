r <- 2; area <- c(2,6)
lambda <- r*area
dpois(0,lambda=lambda)
ppois(5,lambda=lambda,lower.tail=FALSE)
set.seed(405)
k <- rpois(10000,lambda=4)
c(media=mean(k),varianza=var(k))
