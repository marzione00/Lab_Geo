set.seed(17)
x97 <- rlnorm(30, 0, .6)
se97 <- function(B)
  sd(replicate(B,
    mean(sample(x97, replace = TRUE))))
set.seed(717)
s97 <- sapply(c(50, 200, 1000),
  function(B) replicate(12, se97(B)))
s97
