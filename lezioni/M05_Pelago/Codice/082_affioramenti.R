a82 <- split(stazioni$densita,
              stazioni$affioramento)
set.seed(17)
ab82 <- replicate(2000,
  rb74(a82$A) - rb74(a82$B))
mean(a82$A) - mean(a82$B)
quantile(ab82, c(.025, .975),
         type = 7)
