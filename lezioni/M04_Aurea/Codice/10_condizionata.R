# Numeri attesi per 100 casi
t10 <- matrix(c(32,12,8,48), nrow=2,
  dimnames=list(c("B","nonB"),
                c("A","nonA")))
t10
t10["B","A"] / sum(t10["B",])
# Fra tutti i casi: P(A)=44/100
sum(t10[,"A"]) / sum(t10)
