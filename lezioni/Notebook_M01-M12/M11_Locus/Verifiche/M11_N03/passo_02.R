traslate <- sweep(xy,2,c(500000,4980000),"+")
alfa <- pi/6;rotazione <- matrix(c(cos(alfa),sin(alfa),-sin(alfa),cos(alfa)),2,2)
ruotate <- xy%*%rotazione
confronto <- data.frame(trasformazione=c("Traslazione","Rotazione 30 gradi"),
  scarto_massimo_m=c(max(abs(as.matrix(dist(traslate))-D)),max(abs(as.matrix(dist(ruotate))-D))))
confronto
stopifnot(all(confronto$scarto_massimo_m<1e-8))
