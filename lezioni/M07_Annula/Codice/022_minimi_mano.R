# Scarti dalle rispettive medie.
xc <- x - mean(x)
yc <- y - mean(y)
b1 <- sum(xc * yc) / sum(xc^2)
b0 <- mean(y) - b1 * mean(x)
c(intercetta = b0, pendenza = b1)
# Le due procedure devono coincidere.
all.equal(unname(coef(m0)), c(b0, b1))
