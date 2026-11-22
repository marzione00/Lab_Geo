# Due popolazioni adimensionali
set.seed(17)
g54 <- rbinom(500, 1, .65)
mu54 <- ifelse(g54 == 1, 2, 6)
sd54 <- ifelse(g54 == 1, .7, 1)
x54 <- rnorm(500, mu54, sd54)
hist(x54, probability = TRUE,
     main = "Miscela di due gruppi",
     xlab = "X", col = "#E0ECEA")
