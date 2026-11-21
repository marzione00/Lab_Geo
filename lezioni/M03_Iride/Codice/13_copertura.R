# 1: evento; 0: assenza; NA: ignoto
x13 <- c(1, 0, 1, NA, 0, NA)
n13 <- length(x13)
v13 <- sum(!is.na(x13))
e13 <- sum(x13 == 1, na.rm = TRUE)
c(eventi = e13, validi = v13, n = n13)
c(quota_valida = e13 / v13,
  copertura = v13 / n13)
