f <- file.path('dati','campioni_modulo1.csv')
stopifnot(file.exists(f))
d <- read.csv(f,stringsAsFactors=FALSE)
stopifnot(nrow(d)==24,
 !anyDuplicated(d$id),
 all(c('massa_g','volume_cm3') %in% names(d)))
head(d)
