set.seed(17)
B60 <- 2000
i60 <- rbinom(B60, 1, .1)
b60 <- seq_len(B60)
p60 <- cumsum(i60)/b60
plot(b60, p60, type = "l",
     xlab = "Repliche B",
     ylab = "Frequenza cumulativa")
abline(h = .1, col = "#C57E42")
