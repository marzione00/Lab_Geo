set.seed(17)
B58 <- 10000
k58 <- rbinom(B58, 20, .3)
i58 <- k58 >= 8
c(stima = mean(i58),
  esatta = pbinom(7, 20, .3,
    lower.tail = FALSE))
