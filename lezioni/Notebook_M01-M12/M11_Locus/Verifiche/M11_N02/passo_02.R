corretta <- d$lon>8 & d$lon<10 & d$lat>44 & d$lat<46
data.frame(caso=c("Originale","Invertito"),
  lon_primo=c(d$lon[1],invertite$lon[1]),lat_primo=c(d$lat[1],invertite$lat[1]),
  siti_nella_zona=c(sum(corretta),sum(locale)))
stopifnot(all(corretta))
