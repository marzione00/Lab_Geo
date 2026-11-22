casuali <- carica_dati("casuali_comuni_v3.csv");u <- casuali$u
stopifnot(length(u)>=3600L,all(u[1:3600]>=0 & u[1:3600]<1))
ix <- matrix(floor(u[1:3600]*12)+1,300,byrow=TRUE)
b <- apply(ix,1,function(i) mean(v[i]))
q <- quantile(b,c(.025,.975),type=7)
risultato <- data.frame(media=mean(v),basso=unname(q[1]),alto=unname(q[2]),
  repliche=length(b),blocchi=length(v),sd_repliche=sd(b))
risultato
stopifnot(length(b)==300L,all(ix>=1&ix<=12))
