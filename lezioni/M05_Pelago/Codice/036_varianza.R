x36 <- c(4, 5, 6, 9)
sc36 <- x36 - mean(x36)
sum(sc36)  # Scarti vincolati
sum(sc36^2)/(length(x36)-1)
var(x36)   # Stesso denominatore
sd(x36)^2
