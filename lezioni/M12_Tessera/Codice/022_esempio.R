Zm <- Z
Zm[5:8,10:15] <- NA_real_
stopifnot(sum(is.na(Zm))==24)
copertura <- mean(is.finite(Zm))
