x66 <- c(4, 5, 7, 8)
n66 <- length(x66)
B66 <- 2000
set.seed(17)
b66 <- replicate(B66, {
  j <- sample.int(n66, n66,
                  replace = TRUE)
  mean(x66[j])
})
length(b66)  # Una media per replica
