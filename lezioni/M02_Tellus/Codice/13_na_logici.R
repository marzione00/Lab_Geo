# Un confronto puo' essere ignoto
x <- c(2, NA, 5)
x >= 3             # FALSE NA TRUE

# Qui escludiamo il valore assente
ok <- !is.na(x) & x >= 3
stopifnot(!anyNA(ok))
x[ok]              # 5
