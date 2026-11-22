x65 <- c(4, 5, 7, 8)
n65 <- length(x65)
s265 <- var(x65)        # 10/3
v65 <- (n65-1)/n65^2*s265
v65                    # .625
sqrt(v65)              # SE esatto
# Varianza di una sola estrazione
mean((x65-mean(x65))^2)  # 2.5
