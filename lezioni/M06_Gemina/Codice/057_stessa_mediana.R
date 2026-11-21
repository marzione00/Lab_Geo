# Normali teoriche: mediana comune
x57 <- seq(-6,6,length.out=241)
matplot(x57,cbind(dnorm(x57),
        dnorm(x57,0,2)),type="l",
        xlab="Valore",ylab="Densita")
pnorm(0/sqrt(1^2+2^2))  # P(B>A)=.5
