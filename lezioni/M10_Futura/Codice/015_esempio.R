mese_futuro <- rep(1:12,3)
mese_fonte <- rep(cycle(tail(
  train,12)),3)
stopifnot(all(mese_futuro==
              mese_fonte))
