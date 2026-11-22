stretto <- d$x_m>300 & d$x_m<600 & d$y_m>180 & d$y_m<510
data.frame(regola=c("Inclusiva","Stretta"),n=c(sum(dentro),sum(stretto)),
  media=c(mean(d$quota_m[dentro]),mean(d$quota_m[stretto])))
stopifnot(sum(stretto)==90L)
