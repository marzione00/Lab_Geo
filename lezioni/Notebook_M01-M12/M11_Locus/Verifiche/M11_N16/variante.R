piu_ampia <- d$y_m<=500
data.frame(fascia=c("y<=250","y<=500"),n=c(sum(strada),sum(piu_ampia)),
  media=c(mean(d$concentrazione[strada]),mean(d$concentrazione[piu_ampia])))
stopifnot(sum(piu_ampia)==24L)
