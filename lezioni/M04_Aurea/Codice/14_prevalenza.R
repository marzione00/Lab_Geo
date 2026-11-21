prior14 <- c(.1, .4, .8)
pa14 <- .8; pb14 <- .2
pA14 <- pa14*prior14 +
  pb14*(1-prior14)
post14 <- pa14*prior14/pA14
data.frame(prior14, post14)
