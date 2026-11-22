lambda <- eigen(varfit$A,
                only.values=TRUE)$values
Mod(lambda)
stopifnot(all(Mod(lambda)<1))
