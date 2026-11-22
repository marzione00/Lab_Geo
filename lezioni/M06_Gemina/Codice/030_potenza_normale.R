# Due gruppi, sigma noto = 1
se30 <- sqrt(2 / 30)
eta30 <- 0.5 / se30
c30 <- qnorm(0.975)
pnorm(-c30, mean = eta30) +
  pnorm(c30, eta30, lower.tail = FALSE)
