# Una relazione esatta, ma curva.
x <- -3:3
y <- x^2
cor(x, y)              # zero
plot(x, y, pch = 19)
# Rimuovere un punto cambia r:
cor(x[-1], y[-1])
