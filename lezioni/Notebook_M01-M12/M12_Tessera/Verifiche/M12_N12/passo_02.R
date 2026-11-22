errori <- vapply(c(315,135),function(az) {
  luce <- c(sin(az*pi/180)*cos(pi/4),cos(az*pi/180)*cos(pi/4),sin(pi/4))
  attesa <- (-g$gx*luce[1]-g$gy*luce[2]+luce[3])/sqrt(1+g$gx^2+g$gy^2)
  attesa[attesa<0] <- 0
  max(abs(hillshade_esplicito(g$gx,g$gy,az,45)-attesa))
},numeric(1))
data.frame(azimut=c(315,135),errore_massimo=errori)
stopifnot(all(errori<1e-12))
