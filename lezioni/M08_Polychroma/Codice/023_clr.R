# Solo le cinque parti chimiche.
stopifnot(all(comp > 0))
log_comp <- log(comp)
clr <- log_comp - rowMeans(log_comp)
head(clr, 3)
max(abs(rowSums(clr)))
