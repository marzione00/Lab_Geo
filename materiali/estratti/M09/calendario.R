d <- read.csv('dati/co2_1985_2001.csv')
d$data <- as.Date(d$data)
d <- d[order(d$data),]
griglia <- seq(min(d$data),max(d$data),by='month')
stopifnot(identical(d$data,griglia))
stopifnot(!anyNA(d$co2_ppm))
y <- ts(d$co2_ppm,start=c(1985,1),frequency=12)
start(y); end(y); frequency(y)
