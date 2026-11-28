set.seed(2)
l <- rgamma(1e5, 14.147, 5.557)
p <- rbeta(1e5, 4 + 6.685, 5 + 13.354)
c(bayes = mean(1 - exp(-0.5 * l * p)),
  con_stime = 1 - exp(-0.5 * 2.4 * 4 / 9))
