# Stesso tasso: esposizione doppia
L36 <- c(3, 6)
mu36 <- 2 * L36
data.frame(esposizione=L36,
           media=mu36,
           sd=sqrt(mu36),
           cv=1/sqrt(mu36))
