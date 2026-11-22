# c: correlazione sulla scala fisica
c71 <- c(-.7, 0, .7)
a71 <- 1/106
b71 <- .6/40
u71 <- 2.65*sqrt(a71^2+b71^2 -
                 2*c71*a71*b71)
data.frame(c = c71, SD = u71)
