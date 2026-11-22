# mu e s: media e SD originali
rpos <- function(n, mu, s) {
  v <- log1p((s/mu)^2)
  rlnorm(n, log(mu)-v/2, sqrt(v))
}
set.seed(17)
head(rpos(6, mu = 106, s = 1))
