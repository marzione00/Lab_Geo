R_band <- 0.2+0.05*cos(d$y_m/150)
NIR <- 0.4+0.1*sin(d$x_m/180)
stopifnot(all(R_band>=0),all(NIR>=0))
