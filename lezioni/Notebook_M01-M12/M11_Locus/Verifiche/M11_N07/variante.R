altra <- d;altra$concentrazione <- rev(d$concentrazione)
stopifnot(identical(sort(altra$concentrazione),sort(d$concentrazione)))
mappa_valori(altra,"Valori ricollocati, distribuzione marginale invariata")
data.frame(media_originale=mean(d$concentrazione),media_ricollocata=mean(altra$concentrazione))
