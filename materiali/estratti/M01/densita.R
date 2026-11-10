d <- read.csv('dati/campioni_modulo1.csv')
stopifnot(all(d$volume_cm3 > 0))
d$densita <- d$massa_g / d$volume_cm3
aggregate(densita ~ affioramento, d, mean)
