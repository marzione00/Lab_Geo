x <- range(d$x_m[dentro]);y <- range(d$y_m[dentro])
data.frame(asse=c("x","y"),centro_min=c(x[1],y[1]),centro_max=c(x[2],y[2]),
  bordo_min=c(x[1],y[1])-15,bordo_max=c(x[2],y[2])+15)
stopifnot((diff(x)+30)*(diff(y)+30)==sum(dentro)*900)
