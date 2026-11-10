d <- read.csv('dati/temperatura_simulata.csv')
d$data <- as.Date(d$data)
d$mese <- as.integer(format(d$data,'%m'))
b <- subset(d,data<as.Date('2005-01-01'))
r <- aggregate(temperatura_C~mese,b,mean)
d$base <- r$temperatura_C[match(d$mese,r$mese)]
d$anomalia <- d$temperatura_C-d$base
head(d[c('data','temperatura_C','base','anomalia')])
