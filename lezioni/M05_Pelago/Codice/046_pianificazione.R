sigma46 <- 1  # SD pilota, micrometri
E46 <- .1     # Semiampiezza voluta
z46 <- qnorm(.975)
n46 <- ceiling((z46*sigma46/E46)^2)
n46
z46*sigma46/sqrt(n46)
