d <- read.csv('dati/campioni_modulo1.csv')
d$densita <- d$massa_g/d$volume_cm3
f <- tempfile(fileext='.csv')
write.csv(d,f,row.names=FALSE,na='NA')
q <- read.csv(f,na.strings='NA')
stopifnot(identical(q$id,d$id))
e <- abs(q$densita-d$densita)
stopifnot(all(e <= 1e-12+
 1e-10*abs(d$densita)))
unlink(f)
