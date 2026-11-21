set.seed(19057)
u57 <- rnorm(10001)
e57 <- head(u57, -1) * tail(u57, -1)
# Stessa coppia di tempi, due confronti.
cor(head(e57, -1), tail(e57, -1))
cor(head(e57^2, -1), tail(e57^2, -1))
