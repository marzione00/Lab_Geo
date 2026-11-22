# Due regimi con uguale probabilita
set.seed(17)
mu40 <- sample(c(2,10), 10000,
               replace=TRUE)
k40 <- rpois(10000, lambda=mu40)
c(media=mean(k40), varianza=var(k40))
# Teoria: media 6, varianza 6+16=22
