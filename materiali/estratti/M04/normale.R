mu <- 10; sigma <- 2
pnorm(14,mu,sigma)-pnorm(6,mu,sigma)
qnorm(c(.025,.975),mu,sigma)
pnorm(0,mu,sigma)
set.seed(406)
x <- rnorm(10000,mu,sigma)
c(media=mean(x),sd=sd(x))
