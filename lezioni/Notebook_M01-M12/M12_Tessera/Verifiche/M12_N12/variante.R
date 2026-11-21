verifica <- lapply(c(20,70),function(alt) {
  h <- hillshade_esplicito(g$gx,g$gy,315,alt)
  luce <- c(sin(315*pi/180)*cos(alt*pi/180),cos(315*pi/180)*cos(alt*pi/180),sin(alt*pi/180))
  attesa <- (-g$gx*luce[1]-g$gy*luce[2]+luce[3])/sqrt(1+g$gx^2+g$gy^2)
  attesa[attesa<0] <- 0
  data.frame(altezza=alt,media=mean(h),errore=max(abs(h-attesa)))
})
verifica <- do.call(rbind,verifica);verifica
stopifnot(all(verifica$errore<1e-12))
