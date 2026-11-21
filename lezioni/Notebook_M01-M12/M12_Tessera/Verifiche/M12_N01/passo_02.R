dx <- unique(diff(sort(unique(d$x_m))));dy <- unique(diff(sort(unique(d$y_m))))
risultato <- data.frame(asse=c("x","y"),centro_min=c(min(d$x_m),min(d$y_m)),
  centro_max=c(max(d$x_m),max(d$y_m)),passo_m=c(dx,dy),
  bordo_min=c(min(d$x_m)-dx/2,min(d$y_m)-dy/2),
  bordo_max=c(max(d$x_m)+dx/2,max(d$y_m)+dy/2))
risultato
stopifnot(length(dx)==1L,length(dy)==1L,dx==30,dy==30)
