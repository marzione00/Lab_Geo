set.seed(17)
# Una nuova media a ogni replica
m30 <- replicate(200,
  mean(rexp(60, rate = 1)))
hist(m30, main = "200 medie",
     xlab = "Media campionaria")
sd(m30)
1 / sqrt(60)  # SE teorico
