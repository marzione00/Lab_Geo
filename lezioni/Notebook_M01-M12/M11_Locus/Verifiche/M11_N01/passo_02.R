assi <- c("x_m","y_m","lon","lat")
intervalli <- data.frame(asse=assi,
  minimo=vapply(d[assi],min,numeric(1)),massimo=vapply(d[assi],max,numeric(1)),
  unita=c("m locali","m locali","gradi Est","gradi Nord"))
intervalli
data.frame(asse=c("x_m","y_m"),livelli=c(length(unique(d$x_m)),length(unique(d$y_m))),
  passo_m=c(unique(diff(sort(unique(d$x_m)))),unique(diff(sort(unique(d$y_m))))))
