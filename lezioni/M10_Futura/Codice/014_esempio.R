p_stag <- rep(tail(train,12),
              length.out=36)
stopifnot(identical(
  as.numeric(p_stag[1:12]),
  as.numeric(p_stag[13:24])))
