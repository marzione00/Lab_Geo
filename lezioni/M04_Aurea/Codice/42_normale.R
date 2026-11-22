# Modello continuo: media 10, SD 2
x42 <- seq(2, 18, length.out=201)
d42 <- dnorm(x42, mean=10, sd=2)
plot(x42, d42, type="l",
     xlab="x", ylab="Densita")
# dnorm restituisce una densita
dnorm(10, mean=10, sd=2)
