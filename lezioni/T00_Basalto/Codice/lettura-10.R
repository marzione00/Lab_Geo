massa <- c(10,20,30)
volume <- c(4,8,12)
stopifnot(length(massa)==length(volume),
 all(is.finite(massa)),
 all(is.finite(volume)),all(volume>0))
rho <- massa/volume
stopifnot(all(rho==2.5))
rho
