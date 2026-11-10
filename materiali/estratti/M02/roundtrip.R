d <- read.csv('dati/campioni_modulo1.csv')
dir.create('risultati',showWarnings=FALSE)
f <- 'risultati/controllo_esportazione.csv'
write.csv(d,f,row.names=FALSE,na='')
r <- read.csv(f,stringsAsFactors=FALSE)
stopifnot(identical(d$id,r$id))
stopifnot(isTRUE(all.equal(d$massa_g,r$massa_g)))
