rpos <- function(n,mu,s) {
 v <- log1p((s/mu)^2)
 rlnorm(n,log(mu)-v/2,sqrt(v))
}
set.seed(410); B <- 50000L
m <- rpos(B,106,1)
V <- rpos(B,40,.5)
rho <- m/V
quantile(rho,c(.025,.5,.975))
stopifnot(all(m>0),all(V>0))
