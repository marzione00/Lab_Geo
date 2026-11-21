d39 <- mean(b37) - mean(a37)
d0_39 <- 0  # Contrasto sotto H0
t39 <- (d39 - d0_39) / se38
c(stima = d39, SE = se38, t = t39)
