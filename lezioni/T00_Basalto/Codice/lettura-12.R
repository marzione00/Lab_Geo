f <- file.path('dati','campioni_modulo1.csv')
stopifnot(file.exists(f))
d <- read.csv(f,stringsAsFactors=FALSE)
stopifnot(nrow(d)==24,!anyDuplicated(d$id),
 is.numeric(d$massa_g),
 all(is.finite(d$volume_cm3)),
 all(d$volume_cm3>0))
str(d)
