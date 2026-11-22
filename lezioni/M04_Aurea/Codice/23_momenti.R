k23 <- 0:2
p23 <- c(.49, .42, .09)
mu23 <- sum(k23*p23)
v23 <- sum((k23-mu23)^2*p23)
c(media=mu23, varianza=v23,
  sd=sqrt(v23))
# .6, .42, circa .6481
