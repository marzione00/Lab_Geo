w <- diff(diff(train, lag=12))
w2 <- diff(diff(train), lag=12)
stopifnot(isTRUE(all.equal(w,w2)))
length(w)
