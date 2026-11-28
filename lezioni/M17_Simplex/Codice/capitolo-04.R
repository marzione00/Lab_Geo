clr <- function(x) log(x)-mean(log(x))
ait <- function(p,q)
  sqrt(sum((clr(p)-clr(q))^2))
a1 <- c(50,20,15,.1,9.9,5); a2 <- a1
a2[c(1,4)] <- c(49.9,.2)
c1 <- c(50,20,15,5,5,5); c2 <- c1
c2[1:2] <- c(50.1,19.9)
round(c(eu=sqrt(sum((a1-a2)^2)),
  ait_a=ait(a1,a2), ait_c=ait(c1,c2)), 3)
