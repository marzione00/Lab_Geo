# Esempio costruito, senza rumore.
u <- seq(-2, 2, length.out = 101)
v <- u^2
cor(u, v)  # Praticamente zero.
plot(u, v, pch = 16)
