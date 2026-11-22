previsione$ampiezza80 <- 2*qnorm(.9)*previsione$se
previsione[c(1,12,36),c("h","ampiezza80","ampiezza95")]
stopifnot(all(previsione$ampiezza80<=previsione$ampiezza95))
