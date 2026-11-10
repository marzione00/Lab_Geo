d <- read.csv('dati/co2_1985_2001.csv')
y <- ts(d$co2_ppm,start=c(1985,1),frequency=12)
d1 <- diff(y)
d12 <- diff(y,lag=12)
doppia <- diff(d12)
stopifnot(length(doppia)==length(y)-13)
stopifnot(isTRUE(all.equal(
  as.numeric(doppia),as.numeric(diff(d1,lag=12)))))
start(doppia); end(doppia)
