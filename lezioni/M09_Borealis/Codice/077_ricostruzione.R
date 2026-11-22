v77 <- as.numeric(y)
ric77 <- c(v77[1],
           v77[1] + cumsum(diff(v77)))
# Tolleranza dovuta all'aritmetica numerica.
max(abs(ric77 - v77))
stopifnot(max(abs(ric77 - v77)) < 1e-10)
