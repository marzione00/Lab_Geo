d <- read.csv('dati/campioni_modulo1.csv')
sel <- d$affioramento=='A' & d$volume_cm3>=40
s <- d[sel,c('id','massa_g','volume_cm3')]
s <- s[order(s$volume_cm3),]
stopifnot(all(s$id %in% d$id))
s$densita <- s$massa_g / s$volume_cm3
