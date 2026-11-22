# p e' noto in questo esempio
B59 <- c(200, 800, 3200)
p59 <- .1
se59 <- sqrt(p59*(1-p59)/B59)
data.frame(B = B59, SE_MC = se59)
