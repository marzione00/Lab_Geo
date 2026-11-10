d <- read.csv('dati/campioni_modulo1.csv')
d$densita <- d$massa_g / d$volume_cm3
dir.create('risultati',showWarnings=FALSE)
f <- 'risultati/provini_con_densita.csv'
write.csv(d,f,row.names=FALSE)
r <- read.csv(f)
stopifnot(identical(r$id,d$id))
stopifnot(isTRUE(all.equal(r$densita,d$densita)))
