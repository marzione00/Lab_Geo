mu <- 10
phi <- 0.65
c0 <- mu*(1-phi)
stopifnot(all.equal(
  c0/(1-phi), mu))
