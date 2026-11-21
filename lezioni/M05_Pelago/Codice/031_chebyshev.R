n31 <- c(25, 100, 400)
eps31 <- .2  # Tolleranza
# Varianza della popolazione = 1
lim31 <- pmin(1, 1/(n31*eps31^2))
data.frame(n = n31, limite = lim31)
