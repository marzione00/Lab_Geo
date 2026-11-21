delta <- sweep(xy,2,xy[1,],"-")
confronto <- data.frame(asse=c("x","y"),
  massimo_scarto_m=c(max(abs(delta[,1]-d$x_m)),max(abs(delta[,2]-d$y_m))))
confronto
