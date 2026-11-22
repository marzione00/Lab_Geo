# Stessa variabile, tre modelli
x43 <- seq(2, 20, length.out=201)
a43 <- dnorm(x43, 10, 1)
b43 <- dnorm(x43, 10, 2)
c43 <- dnorm(x43, 14, 2)
matplot(x43, cbind(a43,b43,c43),
        type="l", lty=1,
        xlab="x", ylab="Densita")
