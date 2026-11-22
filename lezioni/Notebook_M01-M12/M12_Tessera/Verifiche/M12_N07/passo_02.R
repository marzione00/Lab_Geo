xa <- seq(15,855,60);ya <- seq(15,675,60)
data.frame(asse=c("x","y"),primo_centro=c(xa[1],ya[1]),
  ultimo_centro=c(tail(xa,1),tail(ya,1)),bordo_min=c(xa[1],ya[1])-30,
  bordo_max=c(tail(xa,1),tail(ya,1))+30)
stopifnot(length(A)*60^2==length(Z)*30^2)
