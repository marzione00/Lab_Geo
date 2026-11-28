d <- read.csv('dati/composizioni_v1.csv')
x <- d[4:9]
table(d$litologia, d$sotto_limite)
z <- rowSums(x == 0) > 0
round(range(rowSums(x[z, ])), 2)
