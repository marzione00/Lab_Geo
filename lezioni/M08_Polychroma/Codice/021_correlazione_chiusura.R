set.seed(17)
assolute <- matrix(rlnorm(450), ncol = 3)
frazioni <- assolute / rowSums(assolute)
c(prima = cor(assolute)[1, 2],
  dopo = cor(frazioni)[1, 2])
