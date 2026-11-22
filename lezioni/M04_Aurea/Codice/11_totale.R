prior11 <- .4    # P(B)
pa11 <- .8       # P(A dato B)
pb11 <- .2       # P(A dato nonB)
joint11 <- c(prior11 * pa11,
  (1-prior11) * pb11)
joint11         # .32 e .12
sum(joint11)    # P(A) = .44
