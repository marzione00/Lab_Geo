a <- d$id[d$x_m<=1250]
b <- d$id[d$x_m>=750]
freq <- table(c(a,b))
c(siti=length(freq),
  relazioni=sum(freq),
  multipli=sum(freq>1))
