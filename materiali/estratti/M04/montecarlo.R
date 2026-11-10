set.seed(409)
B <- 50000L
k <- rbinom(B,20,.3)
p_hat <- mean(k>=8)
se <- sqrt(p_hat*(1-p_hat)/B)
p_esatta <- pbinom(7,20,.3,lower.tail=FALSE)
c(stima=p_hat,errore_MC=se,esatta=p_esatta)
