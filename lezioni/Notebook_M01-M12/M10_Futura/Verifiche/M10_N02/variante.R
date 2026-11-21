media <- rep(mean(train),h)
data.frame(metodo=c("Media","Ultimo"),previsione=c(media[1],ultimo[1]))
stopifnot(all(media==mean(train)))
