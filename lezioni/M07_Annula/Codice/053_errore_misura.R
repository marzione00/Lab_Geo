# Esempio classico, tutto simulato.
set.seed(753)
x53 <- rnorm(1000)
y53 <- 2 + 1.5*x53 + rnorm(1000)
w53 <- x53 + rnorm(1000, sd = 0.8)
c(latente = coef(lm(y53 ~ x53))[2],
  misurato = coef(lm(y53 ~ w53))[2])
# Pendenza limite attesa:
1.5 / (1 + 0.8^2)
