x <- 1:3
c(campione=sd(x),
  popolazione=sqrt(mean((x-mean(x))^2)))
