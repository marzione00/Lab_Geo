# X adimensionale, 500 estrazioni
set.seed(17)
x51 <- rlnorm(500, 0, .6)
range(x51)
hist(log(x51), probability = TRUE,
     main = "Logaritmo di X",
     xlab = "log(X)", col = "#E0ECEA")
curve(dnorm(x, 0, .6), add = TRUE,
      col = "#087C74", lwd = 2)
