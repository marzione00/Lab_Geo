d12 <- diff(train, lag=12)
stopifnot(length(d12)==156)
frequency(train)
