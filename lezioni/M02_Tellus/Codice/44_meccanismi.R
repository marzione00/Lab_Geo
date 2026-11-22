set.seed(17)
x_miss <- rlnorm(200, 1, 0.5)
# Due regole, stesso campione
casuali <- runif(200) < 0.3
alti <- rank(x_miss) > 200 * 0.7
c(casuali = sum(casuali),
  selettivi = sum(alti))
