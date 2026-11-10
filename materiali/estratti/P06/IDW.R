d <- read.csv('dati/spazio_v3.csv')
tr <- d$x_m<1250
q <- vapply(which(!tr),function(i){
 r <- sqrt((d$x_m[tr]-d$x_m[i])^2+
           (d$y_m[tr]-d$y_m[i])^2)
 w <- r^-2
 sum(w*d$concentrazione[tr])/sum(w)
},numeric(1))
e <- d$concentrazione[!tr]-q
c(MAE=mean(abs(e)),RMSE=sqrt(mean(e^2)))
