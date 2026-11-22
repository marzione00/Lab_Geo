a18 <- c(1,2,4,5)
b18 <- c(3,5,6,8)
set.seed(17)
# Bootstrap entro ciascun gruppo
mean(sample(b18,4,replace=TRUE)) -
 mean(sample(a18,4,replace=TRUE))
# Permutazione: valori fissi
sample(rep(c("A","B"), each=4))
