set.seed(17)
x15 <- c(rnorm(20),rnorm(20,.6))
g15 <- rep(0:1, each=20)
obs15 <- diff(tapply(x15,g15,mean))
B15 <- 200
t15 <- replicate(B15, {
 gp <- sample(g15)
 diff(tapply(x15,gp,mean))
})
