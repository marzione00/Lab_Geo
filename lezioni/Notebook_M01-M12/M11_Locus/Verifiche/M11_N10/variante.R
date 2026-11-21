dist_angolo <- sqrt(d$x_m^2+d$y_m^2)
s <- dist_angolo<=600
data.frame(centro=c("750,750","0,0"),raggio_m=600,
  n=c(sum(dist0<=600),sum(s)),
  media=c(mean(d$concentrazione[dist0<=600]),mean(d$concentrazione[s])))
