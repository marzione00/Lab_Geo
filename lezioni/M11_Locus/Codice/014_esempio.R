stopifnot(nrow(d)==64L,
 all(is.finite(xy)),
 all(is.finite(z)),
 !anyDuplicated(d$id))
sapply(d[c("x_m","y_m")],range)
