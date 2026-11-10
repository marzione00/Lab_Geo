d <- read.csv('dati/campioni_modulo1.csv')
d$densita <- d$massa_g / d$volume_cm3
table(d$affioramento, d$stazione)
st <- aggregate(densita ~ stazione, d, mean)
c(provini=nrow(d), stazioni=nrow(st))
mean(st$densita)
