falsi <- sf::st_coordinates(sf::st_transform(errato,"OGC:CRS84"))
in_zona <- falsi[,1]>8 & falsi[,1]<10 & falsi[,2]>44 & falsi[,2]<46
risultato <- data.frame(id=d$id,lon_errata=falsi[,1],lat_errata=falsi[,2],nella_zona=in_zona)
head(risultato,4)
data.frame(siti_nella_zona=sum(in_zona),totale=nrow(d))
stopifnot(!any(in_zona))
write.csv(risultato,percorso_risultati("effetto_rietichettatura.csv"),row.names=FALSE)
