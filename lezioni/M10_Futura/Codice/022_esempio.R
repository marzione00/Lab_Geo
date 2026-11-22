b <- baseline(train, h=36)
stopifnot(all(lengths(b)==36))
stopifnot(all(is.finite(
  unlist(b))))
names(b)
