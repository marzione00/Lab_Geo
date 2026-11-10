d <- read.csv('dati/estremi_v3.csv')
x <- d$portata_massima_m3s
q <- 600
F <- mean(x <= q)
p <- mean(x > q)
stopifnot(abs(F+p-1) < 1e-12)
data.frame(soglia=q,CDF=F,superamento=p)
