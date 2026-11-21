z <- c(0,20,50,80,120,160)
t <- c(0,160,450,780,1400,2200)
eta <- approx(z,t,xout=c(60,100))$y
c(eta,durata=diff(eta))
