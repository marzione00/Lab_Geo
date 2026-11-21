zona_larga <- invertite$lon>0 & invertite$lon<50 & invertite$lat>0 & invertite$lat<50
data.frame(siti_errati_accettati=sum(zona_larga),totale=nrow(d))
stopifnot(all(zona_larga))
